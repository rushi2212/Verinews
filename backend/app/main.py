from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import news_routes, user_routes
from utils.config import settings

app = FastAPI(title="Fake News Checker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(news_routes.router, prefix="/api/v1/news", tags=["news"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": "Fake News Checker API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
