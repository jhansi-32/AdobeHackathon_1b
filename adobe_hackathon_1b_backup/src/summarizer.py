from transformers import pipeline

# Load summarizer pipeline ONCE (model is cached locally or in the container)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text, prompt=None, api_key=None):
    """
    Summarizes the given text. If prompt is provided, prepend it for persona effect.
    """
    input_text = f"{prompt}\n{text}" if prompt else text
    # Truncate to avoid exceeding model input limits
    input_text = input_text[:4096]
    result = summarizer(input_text, max_length=200, min_length=30, do_sample=False)
    return result[0]['summary_text']
