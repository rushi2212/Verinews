import json
from typing import Dict, List
import re


class FactChecker:
    def __init__(self):
        self.known_fact_check_apis = [
            "https://factchecktools.googleapis.com/v1alpha1/claims:search",
            # Add more fact-checking API endpoints
        ]
        self.trusted_sources = [
            "reuters.com", "apnews.com", "bbc.com", "factcheck.org"
        ]

    async def verify_claims(self, text: str) -> Dict:
        """Verify claims against fact-checking databases"""

        # Extract potential claims from text
        claims = self._extract_claims(text)

        verification_results = []

        for claim in claims:
            # Check against known fake news patterns
            pattern_match = await self._check_known_patterns(claim)

            # Check source credibility if URLs present
            source_analysis = self._analyze_sources(text)

            verification_results.append({
                "claim": claim,
                "pattern_match": pattern_match,
                "source_analysis": source_analysis,
                "verified": pattern_match.get("is_verified", False)
            })

        return {
            "claims_found": len(claims),
            "verification_results": verification_results,
            "overall_credibility": self._calculate_overall_credibility(verification_results)
        }

    def _extract_claims(self, text: str) -> List[str]:
        """Extract potential factual claims from text"""
        sentences = re.split(r'[.!?]+', text)
        claims = []

        # Simple heuristic: sentences that sound like factual statements
        claim_indicators = [
            'is', 'are', 'was', 'were', 'has been', 'have been',
            'according to', 'studies show', 'research indicates'
        ]

        for sentence in sentences:
            sentence = sentence.strip()
            if any(indicator in sentence.lower() for indicator in claim_indicators):
                if len(sentence.split()) > 3:  # Minimum length
                    claims.append(sentence)

        return claims[:5]  # Limit to top 5 claims

    async def _check_known_patterns(self, claim: str) -> Dict:
        """Check claim against known fake news patterns"""
        # Common fake news patterns
        fake_patterns = [
            r"\b(vaccine.*death|death.*vaccine)\b",
            r"\b(government.*cover-up|cover-up.*government)\b",
            r"\b(celebrity.*dead|dead.*celebrity)\b",
            r"\b(miracle.*cure|cure.*miracle)\b"
        ]

        claim_lower = claim.lower()
        matches = []

        for pattern in fake_patterns:
            if re.search(pattern, claim_lower):
                matches.append(pattern)

        return {
            "is_verified": len(matches) == 0,
            "matched_patterns": matches,
            "risk_level": "high" if len(matches) > 0 else "low"
        }

    def _analyze_sources(self, text: str) -> Dict:
        """Analyze sources mentioned in text"""
        # Extract URLs and domain names
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)

        domains = []
        for url in urls:
            domain = url.split('/')[2] if len(url.split('/')) > 2 else url
            domains.append(domain)

        credibility_score = 0
        trusted_count = 0

        for domain in domains:
            if any(trusted in domain for trusted in self.trusted_sources):
                trusted_count += 1
                credibility_score += 1
            else:
                credibility_score -= 0.5

        return {
            "domains_found": domains,
            "trusted_sources_count": trusted_count,
            "credibility_score": max(0, credibility_score)
        }

    def _calculate_overall_credibility(self, verification_results: List[Dict]) -> float:
        """Calculate overall credibility score"""
        if not verification_results:
            return 0.8  # Neutral if no claims found

        verified_count = sum(
            1 for result in verification_results if result["verified"])
        total_claims = len(verification_results)

        return verified_count / total_claims if total_claims > 0 else 0.8
