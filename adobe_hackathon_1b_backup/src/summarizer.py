from transformers import pipeline
import os

# Suppress deprecation warnings (optional, but cleans up the output)
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Define the cache directory. This is consistent with Dockerfile.
CACHE_DIR = os.environ.get("HF_HOME", "/app/hf_model_cache")

# **IMPORTANT:** REMOVE the global 'summarizer = pipeline(...)' here.
# We will initialize it inside the function for more control.

def summarize_text(text, prompt=None, api_key=None):
    """
    Summarizes the given text. If prompt is provided, prepend it for persona effect.
    """
    # Initialize the summarizer pipeline INSIDE THE FUNCTION.
    # This ensures 'cache_dir' is used for loading and not accidentally passed to 'generate'.
    # Note: This means the model will be loaded (or checked for existence) on every call.
    # For performance, we can add a simple caching mechanism inside the function.
    
    # --- Performance Optimization (Optional, but Recommended) ---
    # Use a simple function-level cache to load the pipeline only once per program run.
    if not hasattr(summarize_text, "_cached_summarizer"):
        summarize_text._cached_summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            cache_dir=CACHE_DIR
        )
    summarizer_instance = summarize_text._cached_summarizer
    # --- End Performance Optimization ---

    input_text = f"{prompt}\n{text}" if prompt else text
    input_text = input_text[:4096] # Truncate to avoid exceeding model input limits

    input_tokens = len(input_text.split())
    max_len = max(30, min(200, int(input_tokens * 0.5))) # Dynamically set max_length

    # Call the summarizer instance
    result = summarizer_instance(input_text, max_length=max_len, min_length=20, do_sample=False)
    
    return result[0]['summary_text']
