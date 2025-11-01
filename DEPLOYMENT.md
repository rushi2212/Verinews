# 🚀 VeriNews Deployment Guide

## Deployment Targets

- **Backend**: Render (FastAPI + Uvicorn)
- **Frontend**: Vercel or Netlify (React + Vite)

---

## 📦 Backend Deployment (Render)

### Prerequisites
- Render account (render.com)
- GitHub repository connected to Render
- API Keys ready:
  - `GOOGLE_API_KEY` (Google Gemini)
  - `TAVILY_API_KEY` (Tavily Search)

### Step 1: Create a Web Service on Render

1. Go to [render.com](https://render.com) and sign in
2. Click **+ New** → **Web Service**
3. Select your GitHub repository (Verinews)
4. Configure:
   - **Name**: `verinews-backend` (or your choice)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or Paid for better performance)

### Step 2: Add Environment Variables

In Render dashboard:
1. Go to your service → **Environment**
2. Add the following variables:

```
GOOGLE_API_KEY = your_gemini_api_key_here
TAVILY_API_KEY = your_tavily_api_key_here
GEMINI_MODEL = gemini-2.5-flash
```

**Security Tip**: Use Render's secret management, never hardcode keys!

### Step 3: Deploy

1. Click **Deploy** button
2. Render will:
   - Clone your GitHub repo
   - Install dependencies from `backend/requirements.txt`
   - Start your service
   - Provide you with a public URL (e.g., `https://verinews-backend.onrender.com`)

### Deployment Time
- **First Deploy**: ~5-10 minutes
- **Subsequent Deploys**: ~2-3 minutes

### Monitoring

After deployment:
1. Check **Logs** for any errors
2. Visit your backend URL in browser:
   ```
   https://your-backend.onrender.com/health
   ```
   Should return: `{"status": "healthy"}`

### Common Issues

**Issue**: Build timeout
- **Solution**: We've removed heavy dependencies (torch, transformers, easyocr). This should now build in <2 minutes.

**Issue**: API returns 503 Service Unavailable
- **Solution**: The free tier Render instance may take time to start. Wait 30 seconds and retry.

**Issue**: API key errors
- **Solution**: Ensure both `GOOGLE_API_KEY` and `TAVILY_API_KEY` are set in Environment variables

---

## 🎨 Frontend Deployment

### Option A: Vercel (Recommended)

1. **Connect Repository**
   ```bash
   npm i -g vercel
   vercel
   ```

2. **Configure Build**
   - Framework: Vite
   - Build Command: `npm run build --prefix frontend`
   - Output Directory: `frontend/dist`

3. **Set Environment Variables**
   - `VITE_API_BASE_URL = https://your-backend.onrender.com`

4. **Deploy**
   ```bash
   vercel --prod
   ```

### Option B: Netlify

1. Connect GitHub repo to Netlify
2. Configure Build Settings:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`
3. Add Environment Variables:
   - `VITE_API_BASE_URL = https://your-backend.onrender.com`
4. Deploy by pushing to main branch

---

## 🔄 CI/CD Pipeline (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy Backend to Render
        run: |
          curl https://api.render.com/deploy/srv-YOUR_SERVICE_ID?key=YOUR_RENDER_API_KEY
      - name: Deploy Frontend to Vercel
        run: |
          npm i -g vercel
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## 📊 Production Checklist

Before going live:

- [ ] Environment variables set on Render
- [ ] Backend `/health` endpoint returns 200
- [ ] Frontend env variable `VITE_API_BASE_URL` points to deployed backend
- [ ] Test all three endpoints:
  - [ ] POST `/api/v1/news/check-text`
  - [ ] POST `/api/v1/news/check-voice`
  - [ ] POST `/api/v1/news/check-image`
- [ ] CORS is working (frontend can reach backend)
- [ ] API keys are valid and not expired
- [ ] Database (if added) is initialized
- [ ] Logging is configured

---

## 🔒 Security in Production

1. **Environment Variables**
   - Never commit `.env` files
   - Use Render's Environment section, not `.env`
   - Rotate API keys regularly

2. **CORS Configuration**
   - Currently allows all origins (for development)
   - Update `main.py` for production:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend-domain.com"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. **Rate Limiting**
   - Add to `main.py` later using `slowapi`:
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

4. **HTTPS**
   - Render automatically provides HTTPS
   - All API calls should use HTTPS

---

## 📈 Monitoring & Logs

### Render Dashboard
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Network usage
- **Events**: Deployment history, errors

### Health Checks
Set up periodic health checks:
```bash
curl https://your-backend.onrender.com/health
```

---

## 🆙 Updates & Rollbacks

### Deploy New Version
```bash
git commit -am "feature: improve verification"
git push origin main
# Render auto-deploys
```

### Rollback to Previous Version
1. Go to Render Dashboard
2. Find previous successful deployment
3. Click **Rollback** button

---

## 💰 Cost Estimation

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Render Backend** | Up to 2GB memory, auto-sleep | $20+/month |
| **Vercel Frontend** | Unlimited deployments | Pay per usage |
| **Tavily API** | 1,000 searches/month free | $0.05 per search |
| **Google Gemini** | $0.075/million tokens | Variable |

---

## 🆘 Troubleshooting Deployment

### Build Failed: "requirements.txt not found"
**Fix**: Ensure `backend/requirements.txt` exists and is in the right location

### Backend responds but frontend CORS error
**Fix**: Update backend CORS to allow your frontend domain

### API returns "Service Unavailable (503)"
**Fix**: Free tier Render instances spin down after 15 mins. Wait for cold start.

### Slow response times
**Fix**: Upgrade to paid Render tier for better performance

### API key errors
**Fix**: Double-check keys in Render Environment variables (no typos!)

---

## 📞 Support

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/deployment/
- **Vite Docs**: https://vitejs.dev/guide/build.html

---

**Happy Deploying! 🚀**

For questions or issues, check the logs or open a GitHub issue.
