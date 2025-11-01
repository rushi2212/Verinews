"""
Retrieval + LLM verification pipeline using Tavily (search) and Gemini (evaluation).

- No third-party HTTP libraries used; relies on Python stdlib (urllib) to avoid new deps.
- Designed to be resilient: if API keys are missing or network fails, returns a skipped result.

Public functions:
- verify_with_osint(text: str) -> dict
  Orchestrates search + LLM evaluation and returns a structured result with verdict, confidence, reasoning, and sources.
"""

from __future__ import annotations

import json
import re
import time
import logging
from typing import List, Dict, Any
from collections import OrderedDict
import hashlib
from urllib import request, error

from utils.config import settings


logger = logging.getLogger(__name__)


STOPWORDS = set(
    [
        "the", "is", "at", "which", "on", "and", "a", "an", "to", "of", "in", "for", "by", "with", "as", "that", "this", "it", "are", "be", "from", "or", "was", "were", "has", "have", "had", "will", "would", "can", "could", "should", "may", "might", "not", "no", "yes", "but", "if", "then", "than", "so", "such", "also", "about", "into", "over",
    ]
)


# Simple LRU cache for verification results to stabilize outputs and reduce latency
_CACHE_MAX = 64
_VERIFY_CACHE: OrderedDict[str, Dict[str, Any]] = OrderedDict()


def _cache_get(key: str) -> Dict[str, Any] | None:
    try:
        val = _VERIFY_CACHE.pop(key)
        # reinsert as most-recently-used
        _VERIFY_CACHE[key] = val
        return val
    except KeyError:
        return None


def _cache_set(key: str, value: Dict[str, Any]) -> None:
    if key in _VERIFY_CACHE:
        _VERIFY_CACHE.pop(key)
    elif len(_VERIFY_CACHE) >= _CACHE_MAX:
        # pop least-recently-used
        _VERIFY_CACHE.popitem(last=False)
    _VERIFY_CACHE[key] = value


def extract_queries(text: str, max_terms: int = 8) -> str:
    """Very simple keyword extractor: prefer Capitalized words and long words, filter stopwords."""
    words = re.findall(r"[A-Za-z][A-Za-z\-']{2,}", text)
    scored = []
    for w in words:
        lw = w.lower()
        if lw in STOPWORDS:
            continue
        score = len(w) + (3 if w[0].isupper() else 0)
        scored.append((score, w))
    scored.sort(reverse=True)
    uniq = []
    seen = set()
    for _, w in scored:
        lw = w.lower()
        if lw not in seen:
            uniq.append(w)
            seen.add(lw)
        if len(uniq) >= max_terms:
            break
    # Build a search query string
    if uniq:
        return " ".join(uniq)
    return text[:200]


def _http_post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: float = 15.0) -> Dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={
                          "Content-Type": "application/json", **headers}, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except error.HTTPError as e:
        err_txt = ""
        try:
            err_txt = e.read().decode("utf-8", errors="ignore")
        except Exception:
            err_txt = ""
        logger.warning("HTTPError %s: %s", e.code, err_txt)
        # propagate details upstream for better diagnostics
        raise RuntimeError(f"HTTP Error {e.code}: {err_txt[:500]}")
    except Exception as e:
        logger.warning("HTTP POST failed: %s", e)
        raise


def tavily_search(query: str, max_results: int = 5, search_depth: str = "advanced") -> Dict[str, Any]:
    api_key = settings.TAVILY_API_KEY
    if not api_key:
        return {"status": "skipped", "reason": "TAVILY_API_KEY not set", "results": []}
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": search_depth,
        "max_results": max_results,
        # optional toggles for richer results without full page fetch
        "include_answer": False,
        "include_images": False,
    }
    try:
        res = _http_post_json(url, payload, headers={})
        results = res.get("results") or []
        # Normalize items to have title, url, content/snippet
        norm = []
        for r in results:
            norm.append({
                "title": r.get("title") or r.get("url") or "",
                "url": r.get("url") or "",
                "snippet": r.get("content") or r.get("snippet") or ""
            })
        return {"status": "ok", "results": norm}
    except Exception as e:
        return {"status": "error", "reason": str(e), "results": []}


def build_factcheck_prompt(claim: str, evidence: List[Dict[str, str]]) -> str:
    sources_block = "\n".join([
        f"- {i+1}. {ev.get('title','').strip()} ({ev.get('url','')})\n  Snippet: {ev.get('snippet','').strip()}" for i, ev in enumerate(evidence)
    ])
    prompt = f"""
You are a precise fact-checking assistant. Your task is to assess the truthfulness of a claim using the provided web evidence.

Claim:
"""
    prompt += claim.strip()
    prompt += """

Evidence (web search results):
"""
    prompt += sources_block
    prompt += """

Instructions:
- Carefully read the claim and compare it with the evidence.
- If evidence clearly supports the claim, label it true. If clearly contradicts, label it false. If evidence is insufficient or mixed, label it uncertain.
- Only rely on the provided evidence; do not invent facts.
- Return ONLY a compact JSON object with this schema and nothing else:
  {
    "verdict": "true|false|uncertain",
    "confidence": 0.0-1.0,
    "reasoning": "short explanation",
    "sources": ["<url>", "<url>"]
  }
"""
    return prompt


def build_claim_extraction_prompt(text: str) -> str:
    prompt = f"""
You extract atomic factual claims from user text for fact-checking. A claim should be specific and verifiable (who/what/when/where). Ignore opinions or questions.

Text:
{text.strip()}

Return ONLY JSON with this schema:
{{
  "claims": [
    {{"text": "<claim as a single sentence>"}},
    ... up to 5 claims
  ]
}}
If no claims, return {{"claims": []}}.
"""
    return prompt


def _hostname(url: str) -> str:
    try:
        # simple hostname extraction
        return re.sub(r"^www\.", "", re.sub(r"^https?://", "", url)).split("/")[0].lower()
    except Exception:
        return ""


# Lightweight domain reputation map; 0..1 where 1 is highly credible
_DOMAIN_REPUTATION: Dict[str, float] = {
    # International outlets
    "reuters.com": 0.95,
    "apnews.com": 0.95,
    "bbc.com": 0.93,
    "nytimes.com": 0.92,
    "washingtonpost.com": 0.9,
    "theguardian.com": 0.9,
    "npr.org": 0.9,
    "bloomberg.com": 0.9,
    "aljazeera.com": 0.85,
    # Fact-checkers
    "snopes.com": 0.95,
    "factcheck.org": 0.95,
    "politifact.com": 0.93,
    # Government/education will be boosted via TLD rule
}


def score_domain(url: str) -> float:
    host = _hostname(url)
    if not host:
        return 0.4
    score = _DOMAIN_REPUTATION.get(host, 0.6)
    # TLD heuristics
    if host.endswith(".gov") or host.endswith(".gov.in"):
        score = max(score, 0.92)
    if host.endswith(".edu"):
        score = max(score, 0.88)
    # common low-credibility heuristics
    low_markers = ["click", "buzz", "viral", "gossip", "tabloid"]
    if any(m in host for m in low_markers):
        score = min(score, 0.45)
    return max(0.0, min(1.0, score))


def gemini_extract_claims(text: str) -> List[str] | None:
    api_key = settings.GOOGLE_API_KEY
    preferred = settings.GEMINI_MODEL or "gemini-2.5-flash"
    models = [
        preferred,
        "gemini-2.5-flash-001",
        "gemini-2.5-flash-latest",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
    ]
    if not api_key:
        return None

    prompt = build_claim_extraction_prompt(text)
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
        try:
            res = _http_post_json(url, payload, headers={})
            out_text = ""
            try:
                cand = (res.get("candidates") or [{}])[0]
                parts = (cand.get("content") or {}).get("parts") or []
                if parts:
                    out_text = parts[0].get("text") or ""
            except Exception:
                out_text = ""
            data = _extract_json_from_text(out_text) or {}
            claims_arr = data.get("claims") or []
            claims = []
            for item in claims_arr:
                t = (item.get("text") if isinstance(
                    item, dict) else str(item)).strip()
                if t:
                    claims.append(t)
            return claims[:5]
        except Exception:
            continue
    return None


def _aggregate_claim_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not results:
        return {
            "verdict": "uncertain",
            "confidence": 0.5,
            "fake_risk": 0.5,
            "overall_credibility": 0.6,
        }
    # Weighted by (model confidence * avg source credibility)
    weights: List[float] = []
    truthiness: List[float] = []  # 1 for true, 0 for false, 0.5 for uncertain
    src_cred: List[float] = []
    for r in results:
        conf = float(r.get("confidence", 0.5))
        sources = r.get("sources") or []
        if sources:
            sc = sum(score_domain(u)
                     for u in sources[:3]) / min(len(sources[:3]), 3)
        else:
            sc = 0.6
        weights.append(max(0.1, conf * (0.5 + 0.5 * sc)))
        src_cred.append(sc)
        v = r.get("verdict")
        if v == "true":
            truthiness.append(1.0)
        elif v == "false":
            truthiness.append(0.0)
        else:
            truthiness.append(0.5)

    total_w = sum(weights) or 1.0
    weighted_truth = sum(w * t for w, t in zip(weights, truthiness)) / total_w
    avg_conf = sum(weights) / (len(weights) or 1)
    avg_src = sum(src_cred) / (len(src_cred) or 1)

    # Map to verdict
    if weighted_truth >= 0.66:
        verdict = "true"
    elif weighted_truth <= 0.34:
        verdict = "false"
    else:
        verdict = "uncertain"

    fake_risk = 1.0 - weighted_truth  # higher risk when less true
    # overall confidence scaled by agreement and source quality
    confidence = max(0.3, min(
        0.98, 0.5 + (abs(weighted_truth - 0.5) * 0.8) * (0.6 + 0.4 * avg_src)))

    return {
        "verdict": verdict,
        "confidence": confidence,
        "fake_risk": max(0.0, min(1.0, fake_risk)),
        "overall_credibility": max(0.0, min(1.0, avg_src)),
    }


def gemini_generate_json(prompt: str) -> Dict[str, Any]:
    api_key = settings.GOOGLE_API_KEY
    preferred = settings.GEMINI_MODEL or "gemini-2.5-flash"
    candidates = [
        preferred,
        "gemini-2.5-flash-001",
        "gemini-2.5-flash-latest",
        "gemini-2.0-flash",
        "gemini-2.0-flash-001",
        "gemini-2.0-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-latest",
    ]
    if not api_key:
        return {"status": "skipped", "reason": "GOOGLE_API_KEY not set"}

    last_err: str | None = None
    for model in candidates:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": prompt}]}
            ]
        }
        try:
            res = _http_post_json(url, payload, headers={})
            # Try to extract text
            text = ""
            try:
                candidates_resp = res.get("candidates") or []
                if candidates_resp:
                    content = candidates_resp[0].get("content") or {}
                    parts = content.get("parts") or []
                    if parts:
                        text = parts[0].get("text") or ""
            except Exception:
                text = ""
            parsed = _extract_json_from_text(text)
            if parsed is None:
                # Model responded but not JSON — treat as error and try next model
                last_err = "Could not parse JSON from model output"
                continue
            return {"status": "ok", "data": parsed, "model_used": model}
        except Exception as e:
            last_err = str(e)
            # try next model
            continue

    return {"status": "error", "reason": last_err or "all models failed", "tried_models": candidates}


def _extract_json_from_text(text: str) -> Dict[str, Any] | None:
    if not text:
        return None
    # Look for fenced code block first
    m = re.search(r"```(?:json)?\s*({[\s\S]*?})\s*```", text)
    if not m:
        # fallback: first JSON object
        m = re.search(r"({[\s\S]*})", text)
    if not m:
        return None
    snippet = m.group(1)
    try:
        return json.loads(snippet)
    except Exception:
        # try to sanitize common issues: trailing commas
        snippet2 = re.sub(r",\s*([}\]])", r"\1", snippet)
        try:
            return json.loads(snippet2)
        except Exception:
            return None


def verify_with_osint(text: str, max_results: int = 5) -> Dict[str, Any]:
    """Run claim extraction, Tavily search and Gemini evaluation to verify text with calibrated metrics."""
    started = time.time()
    if not text or not text.strip():
        return {"status": "skipped", "reason": "empty text"}

    # Cache
    key = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    cached = _cache_get(key)
    if cached is not None:
        return {**cached, "cached": True}

    # 1) Extract claims (best-effort). If unavailable, treat entire text as single claim
    claims = gemini_extract_claims(text) or []
    if not claims:
        claims = [text.strip()]

    per_claim: List[Dict[str, Any]] = []
    # 2) Verify each claim
    for claim in claims[:5]:
        query = extract_queries(claim)
        search_res = tavily_search(query, max_results=max_results)
        evidence = search_res.get("results", [])[:max_results]
        if search_res.get("status") != "ok" or not evidence:
            per_claim.append({
                "claim": claim,
                "status": "skipped",
                "reason": search_res.get("reason") or "no evidence",
                "sources": [],
                "evidence": evidence,
            })
            continue

        prompt = build_factcheck_prompt(claim, evidence)
        eval_res = gemini_generate_json(prompt)
        if eval_res.get("status") != "ok":
            per_claim.append({
                "claim": claim,
                "status": "error",
                "reason": eval_res.get("reason"),
                "sources": [ev.get("url", "") for ev in evidence if ev.get("url")],
                "evidence": evidence,
            })
            continue

        data = eval_res.get("data") or {}
        verdict = str(data.get("verdict", "uncertain")).lower()
        if verdict not in ("true", "false", "uncertain"):
            verdict = "uncertain"
        try:
            confidence = float(data.get("confidence", 0.5))
        except Exception:
            confidence = 0.5
        reasoning = str(data.get("reasoning", "")).strip()
        sources = data.get("sources") or [ev.get(
            "url", "") for ev in evidence if ev.get("url")]

        per_claim.append({
            "claim": claim,
            "status": "ok",
            "verdict": verdict,
            "confidence": max(0.0, min(1.0, confidence)),
            "reasoning": reasoning,
            "sources": sources[:max_results],
            "model_used": eval_res.get("model_used"),
            "evidence": evidence,
        })

    duration_ms = int((time.time() - started) * 1000)

    # 3) Aggregate calibrated metrics
    ok_results = [r for r in per_claim if r.get("status") == "ok"]
    agg = _aggregate_claim_results(ok_results)

    # Final shape (maintain backward-compatible keys)
    result = {
        "status": "ok" if ok_results else (per_claim[0].get("status") if per_claim else "skipped"),
        "verdict": agg["verdict"],
        "confidence": agg["confidence"],
        "fake_risk": agg["fake_risk"],
        "overall_credibility": agg["overall_credibility"],
        "claims_found": len(claims),
        "per_claim": per_claim,
        # include union of top sources from ok claims
        "sources": list({u for r in ok_results for u in (r.get("sources") or [])})[:max_results],
        "duration_ms": duration_ms,
    }

    _cache_set(key, result)
    return result
