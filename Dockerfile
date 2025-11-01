# ====================================
# Stage 1 — Build environment
# ====================================
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (for torch, easyocr, pillow)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ====================================
# Stage 2 — Runtime environment
# ====================================
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder stage
COPY --from=builder /usr/local /usr/local

# Copy project files
COPY . .

# Expose the port used by Uvicorn
EXPOSE 10000

# Set environment variables (Render replaces these automatically)
ENV TAVILY_API_KEY=""
ENV GEMINI_API_KEY=""
ENV GROQ_API_KEY=""

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
