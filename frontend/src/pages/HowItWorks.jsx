import React from "react";
import "./HowItWorks.css";

const HowItWorks = () => {
  const steps = [
    {
      number: 1,
      icon: "📝",
      title: "Input Your Content",
      description:
        "Submit a news claim, article text, voice recording, or image containing news text. VeriNews supports multiple input formats for maximum flexibility.",
    },
    {
      number: 2,
      icon: "🔍",
      title: "Web Search & Evidence",
      description:
        "Our system searches the web in real-time using Tavily Search to find relevant, recent sources and evidence related to your claim.",
    },
    {
      number: 3,
      icon: "🤖",
      title: "AI Analysis",
      description:
        "Google Gemini AI analyzes your claim against the retrieved evidence, identifying fact accuracy, linguistic patterns, and potential bias indicators.",
    },
    {
      number: 4,
      icon: "📊",
      title: "Get Results",
      description:
        "Receive a comprehensive analysis with confidence scores, credible sources, linguistic signals, and clear recommendations on claim authenticity.",
    },
  ];

  const features = [
    {
      icon: "🎤",
      title: "Multi-Language Support",
      description:
        "Verify news in 10+ languages including Hindi, Tamil, Telugu, and more.",
    },
    {
      icon: "🖼️",
      title: "Image Text Recognition",
      description:
        "Extract and verify text from images and screenshots automatically using OCR.",
    },
    {
      icon: "🎯",
      title: "Real-Time Web Search",
      description:
        "Access the latest information to fact-check current events and breaking news.",
    },
    {
      icon: "📈",
      title: "Confidence Scoring",
      description:
        "Get clear probability scores showing how likely a claim is true or false.",
    },
    {
      icon: "🔗",
      title: "Source References",
      description:
        "See all the web sources and links that backed up the analysis results.",
    },
    {
      icon: "⚡",
      title: "Lightning Fast",
      description:
        "Get results in seconds with our optimized AI pipeline and cloud infrastructure.",
    },
  ];

  const workflow = [
    {
      phase: "Input",
      items: [
        "Text claims",
        "Voice recordings",
        "Image uploads",
        "Document screenshots",
      ],
    },
    {
      phase: "Processing",
      items: [
        "Claim extraction",
        "Text normalization",
        "Web evidence retrieval",
        "AI reasoning",
      ],
    },
    {
      phase: "Analysis",
      items: [
        "Fact verification",
        "Source ranking",
        "Linguistic signals",
        "Bias detection",
      ],
    },
    {
      phase: "Results",
      items: [
        "Confidence score",
        "Source links",
        "Recommendations",
        "Detailed findings",
      ],
    },
  ];

  return (
    <div className="how-it-works">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1>How VeriNews Works</h1>
          <p>
            Discover how our AI-powered system verifies news claims across text,
            voice, and images in seconds.
          </p>
        </div>
      </section>

      {/* Steps Section */}
      <section className="steps-section">
        <div className="container">
          <h2>Verification Process</h2>
          <div className="steps-grid">
            {steps.map((step) => (
              <div key={step.number} className="step-card">
                <div className="step-header">
                  <div className="step-icon">{step.icon}</div>
                  <div className="step-number">Step {step.number}</div>
                </div>
                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow Section */}
      <section className="workflow-section">
        <div className="container">
          <h2>Complete Workflow</h2>
          <div className="workflow-grid">
            {workflow.map((phase) => (
              <div key={phase.phase} className="phase-card">
                <h3>{phase.phase}</h3>
                <ul>
                  {phase.items.map((item, idx) => (
                    <li key={idx}>
                      <span className="checkmark">✓</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2>Key Features</h2>
          <div className="features-grid">
            {features.map((feature, idx) => (
              <div key={idx} className="feature-card">
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="tech-section">
        <div className="container">
          <h2>Powered By Latest Technology</h2>
          <div className="tech-grid">
            <div className="tech-card">
              <h3>🤖 Google Gemini API</h3>
              <p>Advanced AI model for reasoning and analysis</p>
            </div>
            <div className="tech-card">
              <h3>🔍 Tavily Search</h3>
              <p>Real-time web search for evidence retrieval</p>
            </div>
            <div className="tech-card">
              <h3>⚡ FastAPI Backend</h3>
              <p>Lightning-fast REST API for processing</p>
            </div>
            <div className="tech-card">
              <h3>⚛️ React Frontend</h3>
              <p>Modern, responsive user interface</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <h2>Ready to Verify News?</h2>
          <p>Start fact-checking in seconds with VeriNews</p>
          <a href="/" className="cta-button">
            Go to Home
          </a>
        </div>
      </section>
    </div>
  );
};

export default HowItWorks;
