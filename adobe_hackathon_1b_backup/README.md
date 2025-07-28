# Persona-Driven Document Summarizer (Offline)

## Overview

This project is an **offline, persona-driven document intelligence system** designed for the Adobe Hackathon Challenge 1B. It processes a set of PDF documents, extracts and ranks the most relevant sections based on a user persona and job-to-be-done, and generates concise, persona-tailored summaries. The system is fully self-contained and does not require any internet connection at runtime.

## Features

- **Offline operation:** All models and dependencies are included; no online API calls.
- **Persona-driven:** Summaries and section rankings are tailored to a specific persona and task.
- **PDF section extraction:** Uses local PDF parsing to identify and extract document sections.
- **Automated summarization:** Employs a local HuggingFace transformer model for summarization.
- **Structured output:** Produces a JSON file with metadata, ranked sections, and refined summaries.

## Technologies Used

- **Python 3.8+**  
  The primary programming language for all scripts and logic.

- **Docker**  
  For containerizing the application, ensuring consistent and portable offline execution across different systems.

- **HuggingFace Transformers**  
  Used for local, offline natural language processing and summarization (`sshleifer/distilbart-cnn-12-6` model).

- **PyTorch**  
  Backend framework for running the transformer model.

- **pdfplumber**  
  For extracting and parsing text and sections from PDF documents.

- **Regex (re module)**  
  For identifying section headings and structuring extracted text.

- **JSON**  
  For input/output data formatting and configuration.

- **OS and sys modules**  
  For file handling, directory management, and system operations.

## Folder Structure

```
adobe_hackathon_1b/
├── data/                   # Input PDF files
├── output/                 # Output JSON file
├── src/                    # Source code
│   ├── persona_intelligence.py
│   ├── utils.py
│   ├── summarizer.py
│   └── persona_prompts.json
├── hf_model_cache/         # Pre-downloaded HuggingFace model (for offline use)
├── requirements.txt
├── Dockerfile
├── challenge1b_input.json  # Input specification
├── README.md
└── approach_explanation.md # (Optional) Methodology explanation
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the Summarization Model (One-Time, With Internet)

If you need to re-download the model, run:
```python
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
AutoModelForSeq2SeqLM.from_pretrained('sshleifer/distilbart-cnn-12-6', cache_dir='./hf_model_cache')
AutoTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6', cache_dir='./hf_model_cache')
```
This will save the model in `hf_model_cache/` for offline use.

### 3. Build the Docker Image (Offline)

```bash
docker build -t persona-summarizer-offline .
```

### 4. Run the Container

```bash
docker run --rm persona-summarizer-offline
```
Or, to map the output to your host:
```bash
docker run --rm -v $(pwd)/output:/app/output persona-summarizer-offline
```

## Input & Output

- **Input:**  
  - Place your PDF files in the `data/` directory.
  - Specify the persona and job in `challenge1b_input.json`.
  - Define persona prompts in `src/persona_prompts.json`.

- **Output:**  
  - The results will be saved in `output/challenge1b_output.json` in the required format.

## Methodology

1. **PDF Section Extraction:**  
   Uses `pdfplumber` and regex to identify section headings and extract text blocks from each PDF.

2. **Section Ranking:**  
   Each section is scored for relevance based on keywords and the persona's job-to-be-done.

3. **Summarization:**  
   The most relevant sections are summarized using a local transformer model (`sshleifer/distilbart-cnn-12-6`), with the persona prompt prepended for context.

4. **Output Structuring:**  
   The top-ranked sections and their summaries are compiled into a structured JSON file, including metadata for reproducibility.

## Notes

- **Offline Guarantee:**  
  All processing, including summarization, is performed locally. No internet connection is required at runtime.
- **Model Cache:**  
  The `hf_model_cache/` directory must be present and contain the required model files for offline operation.
- **Extensibility:**  
  You can add new personas or tasks by editing `src/persona_prompts.json`.

## Contact

For any questions or issues, please contact the project maintainer.
