# ✅ Render Deployment Checklist

## Before Redeploying

- [x] **Lightweight requirements.txt** - Removed heavy ML deps (torch, transformers, easyocr)
- [x] **Minimal dependencies** - Only 6 core packages, builds in ~1 minute
- [x] **Production scripts** - Added start.sh and build.sh
- [x] **Render config** - Created render.json for automated setup
- [x] **Deployment guide** - See DEPLOYMENT.md for full instructions

## ✨ What Changed

### Dependencies Removed (Why)
- ❌ `torch` - Not needed; using Gemini API instead
- ❌ `transformers` - Not needed; using Gemini API instead  
- ❌ `easyocr` - Using Gemini OCR fallback instead
- ❌ `SpeechRecognition` - Frontend handles speech, optional on backend
- ❌ `pydub` - Optional audio processing
- ❌ `Pillow` - Using Gemini for image processing

### Dependencies Kept (Essential)
- ✅ `fastapi` - Web framework
- ✅ `uvicorn[standard]` - ASGI server with extras
- ✅ `python-multipart` - Form data handling
- ✅ `pydantic` - Data validation
- ✅ `python-dotenv` - Environment variables
- ✅ `PyJWT` - JWT authentication

### Build Time Improvement
- **Before**: 10-15 minutes (torch/transformers took forever)
- **After**: ~1 minute (just pip install, no compilation)

## 🚀 Quick Deploy Steps

### 1. Go to Render Dashboard
https://dashboard.render.com

### 2. Create New Web Service
- GitHub repo: `rushi2212/Verinews`
- Branch: `main`

### 3. Configure Service

**Build & Start Commands** (Render auto-fills from git):
```
Build Command: pip install -r backend/requirements.txt
Start Command: cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables**:
```
GOOGLE_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### 4. Deploy
Click **Deploy** - should complete in <3 minutes!

### 5. Verify
```bash
curl https://your-backend.onrender.com/health
# Should return: {"status": "healthy"}
```

## 📊 Expected Build Output

You should see:
```
==> Cloning from https://github.com/rushi2212/Verinews
==> Checking out commit ...
==> Installing Python version 3.13.4...
==> Running build command 'pip install -r backend/requirements.txt'...
Collecting fastapi==0.104.1
Collecting uvicorn==0.24.0
...
Successfully installed fastapi uvicorn python-multipart pydantic python-dotenv PyJWT
==> Build successful!
==> Starting server at 0.0.0.0:PORT
```

## 🎯 Success Indicators

After deployment:
1. ✅ Build completes in <3 minutes
2. ✅ No timeout errors
3. ✅ `/health` endpoint returns 200
4. ✅ API keys are set (check Logs for any missing key errors)
5. ✅ All three endpoints work:
   - `POST /api/v1/news/check-text`
   - `POST /api/v1/news/check-voice`
   - `POST /api/v1/news/check-image`

## 🔧 Test After Deployment

```bash
# Test backend health
curl https://your-backend.onrender.com/health

# Test text verification (requires API keys)
curl -X POST https://your-backend.onrender.com/api/v1/news/check-text \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=NASA landed on moon in 1969&language=en"
```

## ⚠️ Common Deployment Errors (Fixed!)

### ❌ Error: "build timeout" or "took too long"
**Status**: ✅ **FIXED** - Removed heavy dependencies

### ❌ Error: "Pillow installation failed"
**Status**: ✅ **FIXED** - Removed Pillow, using Gemini instead

### ❌ Error: "torch compilation failed"
**Status**: ✅ **FIXED** - Removed torch, using Gemini API

### ❌ Error: "transformers not found"
**Status**: ✅ **FIXED** - Removed transformers, using Gemini API

## 📝 Frontend Deployment

After backend is deployed:

1. **Get your backend URL**: `https://your-backend.onrender.com`

2. **Deploy frontend to Vercel**:
   ```bash
   npm i -g vercel
   cd frontend
   vercel --prod
   # Set VITE_API_BASE_URL = https://your-backend.onrender.com
   ```

3. **Or deploy to Netlify**:
   - Connect GitHub repo to Netlify
   - Set Build: `cd frontend && npm install && npm run build`
   - Set Publish: `frontend/dist`
   - Set env: `VITE_API_BASE_URL=https://your-backend.onrender.com`

## 🆘 Still Having Issues?

1. **Check Render Logs**: Dashboard → Your Service → Logs
2. **Verify env vars**: Dashboard → Your Service → Environment
3. **Test locally**: `cd backend && python -m uvicorn app.main:app --reload`
4. **Check GitHub**: Make sure latest code is pushed to main branch

## 📞 Need Help?

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/deployment/render/
- GitHub Issues: Open an issue with logs

---

**Next Deploy**: Just push to main branch, Render auto-deploys! 🚀
