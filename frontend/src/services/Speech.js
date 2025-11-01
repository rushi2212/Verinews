class SpeechRecognitionService {
  constructor() {
    this.recognition = null;
    this.isListening = false;
    this.finalTranscript = '';
    this.interimTranscript = '';
    this.callbacks = {};
    
    this.initializeRecognition();
  }

  initializeRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      console.error('Speech recognition not supported in this browser');
      return;
    }

    this.recognition = new SpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;
    this.recognition.maxAlternatives = 1;

    this.recognition.onstart = () => {
      this.isListening = true;
      if (this.callbacks.onStart) {
        this.callbacks.onStart();
      }
    };

    this.recognition.onresult = (event) => {
      this.interimTranscript = '';
      
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        
        if (event.results[i].isFinal) {
          this.finalTranscript += transcript + ' ';
          if (this.callbacks.onResult) {
            this.callbacks.onResult(this.finalTranscript);
          }
        } else {
          this.interimTranscript += transcript;
          if (this.callbacks.onInterim) {
            this.callbacks.onInterim(this.interimTranscript);
          }
        }
      }
    };

    this.recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      if (this.callbacks.onError) {
        this.callbacks.onError(event.error);
      }
    };

    this.recognition.onend = () => {
      this.isListening = false;
      if (this.callbacks.onEnd) {
        this.callbacks.onEnd(this.finalTranscript);
      }
    };
  }

  startRecognition(onInterim, onResult, onError, onStart, onEnd, language = 'en-US') {
    if (!this.recognition) {
      onError('Speech recognition not supported');
      return;
    }

    this.callbacks = {
      onInterim,
      onResult,
      onError,
      onStart,
      onEnd
    };

    this.finalTranscript = '';
    this.interimTranscript = '';
    
    this.recognition.lang = language;
    this.recognition.start();
  }

  stopRecognition() {
    if (this.recognition && this.isListening) {
      this.recognition.stop();
    }
  }

  isSupported() {
    return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  }
}

// Create singleton instance
const speechService = new SpeechRecognitionService();

// Export functions for React components
export const startSpeechRecognition = (onInterim, onResult, onError, language = 'en') => {
  const languageMap = {
    'en': 'en-US',
    'hi': 'hi-IN',
    'ta': 'ta-IN',
    'te': 'te-IN',
    'bn': 'bn-IN',
    'mr': 'mr-IN',
    'gu': 'gu-IN',
    'kn': 'kn-IN',
    'ml': 'ml-IN',
    'pa': 'pa-IN'
  };

  speechService.startRecognition(
    onInterim,
    onResult,
    onError,
    () => console.log('Speech recognition started'),
    (finalText) => console.log('Speech recognition ended:', finalText),
    languageMap[language] || 'en-US'
  );
};

export const stopSpeechRecognition = () => {
  speechService.stopRecognition();
};

export const isSpeechRecognitionSupported = () => {
  return speechService.isSupported();
};