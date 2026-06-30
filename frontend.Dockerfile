FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy streamlit frontend files
COPY frontend/ ./frontend

# Expose port
EXPOSE 8501

# Run streamlit binding to Railway's dynamic PORT
CMD ["sh", "-c", "python -m streamlit run frontend/streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
