import React, { useState } from "react";
import "./VoiceInput.css";
import {
  startSpeechRecognition,
  stopSpeechRecognition,
} from "../services/Speech";

const VoiceInput = ({ onResult, language, disabled }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");

  const handleStartListening = () => {
    setIsListening(true);
    setTranscript("");

    startSpeechRecognition(
      (text) => {
        setTranscript(text);
      },
      (finalText) => {
        onResult(finalText);
        setIsListening(false);
      },
      (error) => {
        console.error("Speech recognition error:", error);
        setIsListening(false);
      },
      language
    );
  };

  const handleStopListening = () => {
    stopSpeechRecognition();
    setIsListening(false);
    if (transcript) {
      onResult(transcript);
    }
  };

  return (
    <div className="voice-input">
      <button
        className={`voice-button ${isListening ? "listening" : ""}`}
        onClick={isListening ? handleStopListening : handleStartListening}
        disabled={disabled}
      >
        {isListening ? "🛑 Stop Listening" : "🎤 Start Voice Input"}
      </button>

      {isListening && (
        <div className="listening-indicator">
          <div className="pulse"></div>
          <p>Listening... Speak now</p>
        </div>
      )}

      {transcript && (
        <div className="transcript-preview">
          <p>{transcript}</p>
        </div>
      )}
    </div>
  );
};

export default VoiceInput;
