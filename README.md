# 🔍 VeriNews - AI-Powered Fake News Detection

A full-stack application that uses advanced AI and web search to detect and verify news authenticity in real-time. VeriNews combines OSINT (Open Source Intelligence), LLM-powered fact-checking, and sophisticated linguistic analysis to provide accurate credibility assessments.

## ✨ Features

### Core Verification Pipeline

- 🌐 **Web Search Integration** - Uses Tavily API for deep web search to find credible sources
- 🤖 **LLM Fact-Checking** - Google Gemini analyzes claims against web evidence
- 📊 **Multi-Claim Verification** - Extracts and verifies multiple atomic claims per submission
- 🎯 **Domain Credibility Scoring** - Weighs sources by reputation and TLD (.gov, .edu, etc.)
- 💾 **Result Caching** - LRU cache for stable, fast results on repeated checks

### Input Methods

- 📝 **Text Input** - Paste news articles or social media posts
- 🎙️ **Voice Input** - Speech-to-text with automatic analysis
- 🖼️ **Image/OCR** - Extract text from images and verify (with Gemini fallback)

### Analysis Features

- **Sentiment Analysis** - Keyword-based emotion detection (positive/negative/neutral)
- **Fake News Risk Scoring** - Rule-based detection of sensationalism, emotional appeals, vague language
- **Linguistic Analysis** - Urgency scores, emotional language, clickbait detection
- **Source Verification** - Display credible sources backing the verdict
- **Risk Recommendations** - Actionable guidance based on credibility level

## 🎨 Modern UI/UX

- **Glassmorphism Design** - Premium frosted-glass card aesthetic
- **Real-time Updates** - Smooth animations and instant feedback
- **Responsive Layout** - Mobile-first design that scales beautifully
- **Rich Metrics Display** - Color-coded cards, progress bars, verdict badges
- **Tabbed Interface** - Easy switching between text, voice, and image modes

## 🏗️ Architecture

### Backend (FastAPI + Python)

```txt
backend/
├── app/
│   ├── main.py              # FastAPI app setup
│   ├── models/              # Data models
│   ├── routes/
│   │   ├── news_routes.py   # /api/v1/news/* endpoints
│   │   └── user_routes.py   # User management
│   └── services/
│       ├── ai_analyzer.py   # Rule-based text analysis + OCR
│       ├── fact_checker.py  # Legacy fact-check patterns
│       ├── retrieval_verifier.py  # Tavily + Gemini OSINT pipeline
│       └── speech_processor.py    # Speech-to-text
├── utils/
│   └── config.py            # Settings and environment variables
└── requirements.txt         # Python dependencies
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/
│   │   ├── NewsChecker.jsx  # Main input interface
│   │   ├── Results.jsx      # Results display
│   │   ├── VoiceInput.jsx   # Speech recognition
│   │   └── *.css            # Component styles
│   ├── pages/               # Page layouts
│   ├── services/
│   │   ├── api.js           # Backend API calls
│   │   └── Speech.js        # Speech API wrapper
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── package.json
└── vite.config.js
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- API Keys:
  - Google Gemini API (`GOOGLE_API_KEY`)
  - Tavily Search API (`TAVILY_API_KEY`)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   Create a `.env` file in the `backend/` directory:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   GEMINI_MODEL=gemini-2.5-flash
   ```

5. **Run the server**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   Server will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create environment file**
   Create a `.env` file in the `frontend/` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

## 📚 API Documentation

### Check Text News
**Endpoint:** `POST /api/v1/news/check-text`

**Request:**
```json
{
  "text": "NASA landed on the moon in 1969",
  "language": "en"
}
```

**Response:**
```json
{
  "status": "success",
  "analysis": {
    "text_metrics": {...},
    "sentiment": {"label": "NEUTRAL", "score": 0.5},
    "fake_news_probability": 0.25,
    "risk_level": "low",
    "confidence_score": 0.84
  },
  "verification": {
    "status": "ok",
    "verdict": "true",
    "confidence": 0.836,
    "fake_risk": 0.0,
    "overall_credibility": 0.6,
    "claims_found": 1,
    "per_claim": [...],
    "sources": ["https://en.wikipedia.org/wiki/Moon_landing", ...],
    "reasoning": "Multiple sources confirm..."
  }
}
```

### Check Voice News
**Endpoint:** `POST /api/v1/news/check-voice`

**Request:** (multipart/form-data)
- `audio_file`: Audio file (WAV, MP3, OGG, etc.)
- `language`: Language code (default: "en")

**Response:** Same structure as text check

### Check Image News
**Endpoint:** `POST /api/v1/news/check-image`

**Request:** (multipart/form-data)
- `image_file`: Image file (JPG, PNG, etc.)
- `text`: Optional additional context
- `language`: Language code (default: "en")

**Response:** Same structure as text check, includes `extracted_text` field

## 🔧 Configuration

### Backend Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaSyD...` |
| `TAVILY_API_KEY` | Tavily search API key | `tvly-...` |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.5-flash` |

### Frontend Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `http://localhost:8000` |

## 📊 How It Works

### Verification Pipeline

1. **Claim Extraction**
   - Gemini extracts 1-5 atomic claims from input text
   - Each claim is independently verifiable

2. **OSINT Search**
   - For each claim, Tavily performs deep web search
   - Collects evidence from credible sources

3. **LLM Evaluation**
   - Gemini analyzes each claim against evidence
   - Returns verdict: true/false/uncertain
   - Provides confidence score and reasoning

4. **Aggregation**
   - Weighted voting across claims
   - Domain reputation scoring
   - Calculates overall verdict and metrics

5. **Caching**
   - Results stored in LRU cache
   - Stabilizes outputs for repeated checks
   - Reduces API latency

## 🎯 Key Metrics Explained

- **Overall Confidence** (%)
  - Combined confidence from all verified claims
  - Weighted by source credibility
  
- **Fake News Risk** (%)
  - Aggregated risk across all claims
  - Higher = more likely to be misinformation
  
- **Claims Found**
  - Number of atomic claims extracted
  - Each verified independently
  
- **Source Credibility** (%)
  - Average reputation of sources
  - Boosted for .gov/.edu domains
  - Penalized for low-quality domains

## 🛠️ Development

### Running Tests
```bash
# Backend tests (if available)
pytest

# Frontend tests
npm test
```

### Code Quality
```bash
# Python linting
pylint app/

# Frontend linting
npm run lint
```

### Building for Production

**Backend:**
```bash
# No build needed, just run:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
npm run build
# Output in dist/ directory
```

## 📦 Dependencies

### Backend
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - Form data parsing
- `PyJWT` - JWT authentication
- `python-dotenv` - Environment variables
- `pydantic` - Data validation

### Frontend
- `react` - UI library
- `vite` - Build tool
- `tailwindcss` - Utility CSS (optional)

## 🔒 Security Considerations

1. **API Keys** - Always use environment variables, never commit keys
2. **CORS** - Currently allows all origins (configure in production)
3. **Input Validation** - Pydantic models validate all inputs
4. **Rate Limiting** - Consider adding for production use
5. **HTTPS** - Use HTTPS in production deployments

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Use different port
python -m uvicorn app.main:app --port 8001
```

**Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

**API key errors:**
- Verify `GOOGLE_API_KEY` and `TAVILY_API_KEY` are set
- Check key validity in respective dashboards

### Frontend Issues

**CORS errors:**
- Ensure backend is running on `http://localhost:8000`
- Check `VITE_API_BASE_URL` in frontend `.env`

**Module not found:**
```bash
npm install
npm cache clean --force
```

**Port 5173 in use:**
```bash
npm run dev -- --port 3000
```

## 📈 Performance Tips

1. **Caching** - Recheck same text for instant results
2. **Batch Processing** - Process multiple checks simultaneously
3. **CDN** - Host frontend assets on CDN for production
4. **Database** - Add persistence layer for result history
5. **Rate Limiting** - Implement throttling to manage API usage

## 🚀 Future Enhancements

- [ ] User accounts and verification history
- [ ] Real-time trending news monitoring
- [ ] Multi-language support (currently basic)
- [ ] Browser extension for inline verification
- [ ] Social media integration (Twitter, Facebook, etc.)
- [ ] Advanced sentiment analysis with transformers
- [ ] Custom source reputation database
- [ ] API rate limiting and authentication
- [ ] Data persistence and analytics dashboard
- [ ] Community fact-checking votes

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section above

## 🙏 Acknowledgments

- **Google Gemini API** - LLM and OCR capabilities
- **Tavily API** - Web search and OSINT
- **React & Vite** - Frontend framework and build tool
- **FastAPI** - Backend framework

---

**Made with ❤️ for accurate news verification**

Built to combat misinformation and promote media literacy in the digital age.
