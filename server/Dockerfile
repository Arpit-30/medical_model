# Base image
FROM python:3.10-slim

WORKDIR /app

# 📦 Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 📁 Copy project files
COPY . /app

# 📦 Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    scikit-learn \
    pandas

# 🌐 Set PYTHONPATH
ENV PYTHONPATH="/app"

# ❤️ Health check (updated endpoint)
HEALTHCHECK CMD curl -f http://localhost:8000/docs || exit 1

# 🚀 Run FastAPI server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]