# Use a small yet compatible Python base image
FROM python:3.10-slim

WORKDIR /app

# Install OS dependencies (for packages like torch)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all source code and resource files
COPY src ./src
COPY challenge1b_input.json .
COPY src/persona_prompts.json ./src/persona_prompts.json
COPY data ./data

# Download and cache the summarization model at build time (key for offline!)
RUN python -c "from transformers import pipeline; pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')"

# Set environment variable to disable tokenizers parallelism warning
ENV TOKENIZERS_PARALLELISM=false

# Expose any needed ports (optional, only for web API/GUI)
# EXPOSE 5000

# Set script to run on container startup
ENTRYPOINT ["python", "src/persona_intelligence.py"]
