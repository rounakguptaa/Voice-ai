FROM python:3.11-slim

# Install system dependencies including ffmpeg for Whisper
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download SentenceTransformer model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Pre-download OpenAI Whisper base model
RUN python -c "import whisper; whisper.load_model('base')"

# Copy application files
COPY backend/ ./backend
COPY syllabus_data/ ./syllabus_data
COPY ncert_chunks.json .

# Expose port
EXPOSE 8000

# Run uvicorn server binding to Railway's dynamic PORT
CMD ["sh", "-c", "python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
