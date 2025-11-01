import React from "react";
import "./Results.css";

const Results = ({ data }) => {
  if (!data) return null;

  console.log("📋 Results component received data:", data);
  // Defensive destructuring with defaults
  const {
    analysis = {},
    fact_check = {},
    confidence_score = 0,
    verification = null,
  } = data;
  const riskLevel = analysis?.risk_level || "unknown";

  const getRiskColor = (level) => {
    switch (level) {
      case "high":
        return "#ff4444";
      case "medium":
        return "#ffaa00";
      case "low":
        return "#00c851";
      default:
        return "#33b5e5";
    }
  };

  const getRiskMessage = (level) => {
    switch (level) {
      case "high":
        return "High Risk - Likely Misinformation";
      case "medium":
        return "Medium Risk - Verify Sources";
      case "low":
        return "Low Risk - Appears Credible";
      default:
        return "Analysis Inconclusive";
    }
  };

  return (
    <div className="results">
      <div className="results-header">
        <h2>🔍 Analysis Results</h2>
        <div className="analysis-badge">AI-Powered Verification</div>
      </div>

      {data.extracted_text && data.extracted_text.length > 0 && (
        <div className="extracted-text-card glass-card">
          <div className="card-header">
            <h4>📄 Extracted Text (from Image)</h4>
          </div>
          <pre className="extracted-text-content">{data.extracted_text}</pre>
        </div>
      )}

      <div className="risk-indicator-card" data-risk={riskLevel}>
        <div className="risk-icon">
          {riskLevel === "high" ? "⚠️" : riskLevel === "medium" ? "⚡" : "✅"}
        </div>
        <div className="risk-content">
          <h3 className="risk-title">{getRiskMessage(riskLevel)}</h3>
          <div className="confidence-bar">
            <div className="confidence-label">Overall Confidence</div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${confidence_score * 100}%`,
                  backgroundColor: getRiskColor(riskLevel),
                }}
              ></div>
            </div>
            <span className="confidence-value">
              {(confidence_score * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      <div className="analysis-cards">
        <div className="metrics-card glass-card">
          <h4>📊 Key Metrics</h4>
          <div className="metrics-grid">
            <div className="metric-item">
              <div className="metric-icon">🚨</div>
              <div className="metric-content">
                <span className="metric-label">Fake News Risk</span>
                <span className="metric-value red">
                  {(
                    ((verification && verification.fake_risk) ??
                      analysis.fake_news_probability ??
                      0) * 100
                  ).toFixed(1)}
                  %
                </span>
              </div>
            </div>

            <div className="metric-item">
              <div className="metric-icon">😊</div>
              <div className="metric-content">
                <span className="metric-label">Sentiment</span>
                <span className="metric-value neutral">
                  {analysis.sentiment?.label || "Neutral"}
                </span>
              </div>
            </div>

            <div className="metric-item">
              <div className="metric-icon">📋</div>
              <div className="metric-content">
                <span className="metric-label">Claims Found</span>
                <span className="metric-value blue">
                  {verification?.claims_found ?? fact_check?.claims_found ?? 0}
                </span>
              </div>
            </div>

            <div className="metric-item">
              <div className="metric-icon">🔗</div>
              <div className="metric-content">
                <span className="metric-label">Source Credibility</span>
                <span className="metric-value green">
                  {(
                    ((verification && verification.overall_credibility) ??
                      fact_check?.overall_credibility ??
                      0) * 100
                  ).toFixed(1)}
                  %
                </span>
              </div>
            </div>
          </div>
        </div>

        {verification && (
          <div className="verification-card glass-card">
            <div className="card-header">
              <h4>🌐 Web Verification</h4>
              <span className="verification-badge">Tavily + Gemini</span>
            </div>
            {verification.status === "ok" ? (
              <div className="verification-content">
                <div className="verdict-section">
                  <div className="verdict-label">Verdict:</div>
                  <div
                    className={`verdict-value verdict-${verification.verdict}`}
                  >
                    {verification.verdict === "true"
                      ? "✅ TRUE"
                      : verification.verdict === "false"
                      ? "❌ FALSE"
                      : "❓ UNCERTAIN"}
                  </div>
                  <div className="confidence-mini">
                    {(verification.confidence * 100).toFixed(1)}% confidence
                  </div>
                </div>

                {verification.reasoning && (
                  <div className="reasoning-section">
                    <strong>💭 Reasoning:</strong>
                    <p>{verification.reasoning}</p>
                  </div>
                )}

                {verification.sources && verification.sources.length > 0 && (
                  <div className="sources-section">
                    <strong>📚 Sources:</strong>
                    <div className="sources-list">
                      {verification.sources.slice(0, 3).map((url, i) => (
                        <a
                          key={i}
                          href={url}
                          target="_blank"
                          rel="noreferrer"
                          className="source-link"
                        >
                          🔗 {new URL(url).hostname}
                        </a>
                      ))}
                      {verification.sources.length > 3 && (
                        <span className="more-sources">
                          +{verification.sources.length - 3} more sources
                        </span>
                      )}
                    </div>
                  </div>
                )}

                {Array.isArray(verification.per_claim) &&
                  verification.per_claim.length > 0 && (
                    <div className="sources-section">
                      <strong>🧩 Claims Checked:</strong>
                      <div className="sources-list">
                        {verification.per_claim.slice(0, 5).map((pc, idx) => (
                          <div key={idx} className="claim-item">
                            <div className="claim-header">
                              <span className="claim-number">#{idx + 1}</span>
                              <span
                                className={`claim-status ${
                                  pc.verdict === "true"
                                    ? "verified"
                                    : pc.verdict === "false"
                                    ? "unverified"
                                    : ""
                                }`}
                              >
                                {pc.verdict === "true"
                                  ? "✅ True"
                                  : pc.verdict === "false"
                                  ? "❌ False"
                                  : "❓ Uncertain"}
                              </span>
                            </div>
                            <p className="claim-text">{pc.claim || ""}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
              </div>
            ) : (
              <div className="verification-fallback">
                <div className="status-indicator">
                  <span className="status-icon">⚠️</span>
                  <span>Verification {verification.status}</span>
                </div>
                {verification.reason && (
                  <p className="reason-text">{verification.reason}</p>
                )}
              </div>
            )}
          </div>
        )}

        {fact_check?.verification_results &&
          fact_check.verification_results.length > 0 && (
            <div className="claims-card glass-card">
              <h4>🔍 Claim Analysis</h4>
              <div className="claims-list">
                {fact_check.verification_results.map((result, index) => (
                  <div key={index} className="claim-item">
                    <div className="claim-header">
                      <span className="claim-number">#{index + 1}</span>
                      <span
                        className={`claim-status ${
                          result.verified ? "verified" : "unverified"
                        }`}
                      >
                        {result.verified ? "✅ Verified" : "❌ Unverified"}
                      </span>
                    </div>
                    <p className="claim-text">{result.claim || "N/A"}</p>
                    {result.matched_patterns &&
                      result.matched_patterns.length > 0 && (
                        <div className="patterns">
                          <strong>Patterns:</strong>{" "}
                          {result.matched_patterns.join(", ")}
                        </div>
                      )}
                  </div>
                ))}
              </div>
            </div>
          )}

        <div className="linguistic-card glass-card">
          <h4>🔤 Linguistic Analysis</h4>
          <div className="linguistic-grid">
            <div className="linguistic-item">
              <span className="linguistic-icon">⚡</span>
              <span className="linguistic-label">Urgency Score</span>
              <span className="linguistic-value">
                {analysis.linguistic_features?.urgency_score || 0}
              </span>
            </div>
            <div className="linguistic-item">
              <span className="linguistic-icon">😤</span>
              <span className="linguistic-label">Emotional Score</span>
              <span className="linguistic-value">
                {analysis.linguistic_features?.emotional_score || 0}
              </span>
            </div>
            <div className="linguistic-item">
              <span className="linguistic-icon">❓</span>
              <span className="linguistic-label">Vague References</span>
              <span className="linguistic-value">
                {analysis.linguistic_features?.vague_references || 0}
              </span>
            </div>
            <div className="linguistic-item">
              <span className="linguistic-icon">🎯</span>
              <span className="linguistic-label">Clickbait</span>
              <span className="linguistic-value">
                {analysis.linguistic_features?.has_clickbait ? "Yes" : "No"}
              </span>
            </div>
          </div>
        </div>

        <div className="recommendations-card glass-card">
          <h4>💡 Recommendations</h4>
          <div className="recommendations-list">
            {riskLevel === "high" && (
              <>
                <div className="recommendation-item high">
                  <span className="rec-icon">❌</span>
                  <span>Do not share this content</span>
                </div>
                <div className="recommendation-item high">
                  <span className="rec-icon">🔍</span>
                  <span>Verify with trusted news sources</span>
                </div>
                <div className="recommendation-item high">
                  <span className="rec-icon">⚠️</span>
                  <span>Report if it violates platform policies</span>
                </div>
              </>
            )}
            {riskLevel === "medium" && (
              <>
                <div className="recommendation-item medium">
                  <span className="rec-icon">⚠️</span>
                  <span>Verify before sharing</span>
                </div>
                <div className="recommendation-item medium">
                  <span className="rec-icon">🔍</span>
                  <span>Check multiple sources</span>
                </div>
                <div className="recommendation-item medium">
                  <span className="rec-icon">📚</span>
                  <span>Look for official statements</span>
                </div>
              </>
            )}
            {riskLevel === "low" && (
              <>
                <div className="recommendation-item low">
                  <span className="rec-icon">✅</span>
                  <span>Content appears credible</span>
                </div>
                <div className="recommendation-item low">
                  <span className="rec-icon">🔍</span>
                  <span>Still recommend source verification</span>
                </div>
                <div className="recommendation-item low">
                  <span className="rec-icon">📢</span>
                  <span>Share responsibly</span>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Results;
