import React, { useState } from "react";
import "./NewsChecker.css";
import VoiceInput from "./VoiceInput";
import { checkNewsText, checkNewsVoice, checkNewsImage } from "../services/api";

const NewsChecker = ({ onAnalysisComplete, loading, setLoading, language }) => {
  const [inputText, setInputText] = useState("");
  const [activeTab, setActiveTab] = useState("text");

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!inputText.trim()) return;

    console.log("📝 Submitting text for analysis:", inputText);
    setLoading(true);
    try {
      const results = await checkNewsText(inputText, language);
      console.log("📊 Analysis complete, passing results to parent:", results);
      onAnalysisComplete(results);
    } catch (error) {
      console.error("Error analyzing text:", error);
      alert("Error analyzing news. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceResult = async (text) => {
    setInputText(text);
    setLoading(true);
    try {
      const results = await checkNewsText(text, language);
      onAnalysisComplete(results);
    } catch (error) {
      console.error("Error analyzing voice input:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    try {
      const results = await checkNewsImage(file, inputText, language);
      onAnalysisComplete(results);
    } catch (error) {
      console.error("Error analyzing image:", error);
      alert("Error analyzing image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="news-checker">
      <h2>Check News Authenticity</h2>

      <div className="tab-navigation">
        <button
          className={activeTab === "text" ? "active" : ""}
          onClick={() => setActiveTab("text")}
        >
          Text Input
        </button>
        <button
          className={activeTab === "voice" ? "active" : ""}
          onClick={() => setActiveTab("voice")}
        >
          Voice Input
        </button>
        <button
          className={activeTab === "image" ? "active" : ""}
          onClick={() => setActiveTab("image")}
        >
          Image/OCR
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "text" && (
          <form onSubmit={handleTextSubmit} className="text-input-form">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste news text or social media post here..."
              rows="6"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !inputText.trim()}>
              {loading ? "Analyzing..." : "Check Authenticity"}
            </button>
          </form>
        )}

        {activeTab === "voice" && (
          <div className="voice-input-section">
            <VoiceInput
              onResult={handleVoiceResult}
              language={language}
              disabled={loading}
            />
            {inputText && (
              <div className="voice-preview">
                <h4>Transcribed Text:</h4>
                <p>{inputText}</p>
              </div>
            )}
          </div>
        )}

        {activeTab === "image" && (
          <div className="image-input-section">
            <input
              type="file"
              accept="image/*,.pdf"
              onChange={handleImageUpload}
              disabled={loading}
            />
            <p>Upload an image or PDF containing news text</p>

            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Additional context (optional)..."
              rows="3"
              disabled={loading}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default NewsChecker;
