import React, { useState } from "react";
import { Routes, Route } from "react-router-dom";
import "./App.css";
import Header from "./components/Header";
import NewsChecker from "./components/NewsChecker";
import Results from "./components/Results";
import LanguageSelector from "./components/LanguageSelector";
import HowItWorks from "./pages/HowItWorks";

function Home() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");

  const handleAnalysisComplete = (analysisResults) => {
    setResults(analysisResults);
  };

  return (
    <>
      <div className="container">
        <div className="language-selector-container">
          <LanguageSelector
            selectedLanguage={language}
            onLanguageChange={setLanguage}
          />
        </div>

        <div className="main-content">
          <div className="input-section">
            <NewsChecker
              onAnalysisComplete={handleAnalysisComplete}
              loading={loading}
              setLoading={setLoading}
              language={language}
            />
          </div>

          <div className="results-section">
            {results && <Results data={results} />}
          </div>
        </div>
      </div>
    </>
  );
}

function App() {
  return (
    <div className="App">
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/how-it-works" element={<HowItWorks />} />
      </Routes>
    </div>
  );
}

export default App;
