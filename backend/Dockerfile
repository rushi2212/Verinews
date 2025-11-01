# Use a stable Python base with known wheel availability
FROM python:3.10-slim

# Avoid prompts and set LANG
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system deps needed for some Python packages (adjust as needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libsndfile1 \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /srv/backend

# Copy requirements first (for better layer caching)
COPY backend/requirements.txt .

# Upgrade pip and install wheels first
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# Copy app sources
COPY backend/ ./ 

# Expose the port (Render will set PORT env)
EXPOSE 8000

# Run the app — use PORT env variable (Render provides $PORT)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
