# Use a small yet compatible Python base image
FROM python:3.10-slim

WORKDIR /app

# Install OS dependencies (for packages like torch)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies with pinned versions for stability
RUN pip install --upgrade pip && \
    pip install --no-cache-dir "transformers==4.37.2" "huggingface_hub==0.23.3" torch pdfplumber python-docx

# Create a dedicated directory for Hugging Face models and ensure proper permissions
RUN mkdir -p /app/hf_model_cache && chmod -R 777 /app/hf_model_cache

# Set environment variables for Hugging Face to use this specific cache directory
ENV HF_HOME=/app/hf_model_cache
ENV TRANSFORMERS_CACHE=/app/hf_model_cache

# Copy all source code and resource files
COPY src ./src
COPY challenge1b_input.json .
COPY src/persona_prompts.json ./src/persona_prompts.json
COPY data ./data

# Download the ENTIRE model repository (including chat templates and extras) at build time
RUN python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='sshleifer/distilbart-cnn-12-6', cache_dir='/app/hf_model_cache', allow_patterns=['*'])"

# Test-load the model to ensure it's usable offline
RUN python -c "from transformers import pipeline; pipeline('summarization', model='sshleifer/distilbart-cnn-12-6', cache_dir='/app/hf_model_cache')"

# Set environment variable to disable tokenizers parallelism warning
ENV TOKENIZERS_PARALLELISM=false

# Set script to run on container startup
ENTRYPOINT ["python", "src/persona_intelligence.py"]

# Set the HuggingFace cache directory
ENV HF_HOME=/app/hf_model_cache

# Copy the local model cache into the image
COPY hf_model_cache /app/hf_model_cache
