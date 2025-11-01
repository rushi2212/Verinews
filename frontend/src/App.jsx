import React, { useState } from "react";
import "./App.css";
import Header from "./components/Header";
import NewsChecker from "./components/NewsChecker";
import Results from "./components/Results";
import LanguageSelector from "./components/LanguageSelector";

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("en");

  const handleAnalysisComplete = (analysisResults) => {
    setResults(analysisResults);
  };

  return (
    <div className="App">
      <Header />

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
    </div>
  );
}

export default App;
