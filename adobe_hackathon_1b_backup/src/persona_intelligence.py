import json
import os
import sys
from datetime import datetime
from utils import extract_pdf_sections
from summarizer import summarize_text

# List of keywords to score section importance (tailor to your task/domain)
IMPORTANCE_KEYWORDS = [
    "itinerary", "things to do", "activities", "adventure", "nightlife",
    "culture", "cuisine", "food", "restaurant", "tips", "advice", "packing",
    "hotel", "transport", "must-see", "group", "travel"
]

def score_importance(section_title, section_text, persona_job):
    """Simple scoring: count how many keywords appear in title/text."""
    text = (section_title or "") + " " + (section_text or "") + " " + persona_job
    score = sum(kw.lower() in text.lower() for kw in IMPORTANCE_KEYWORDS)
    # Bonus for keywords in title
    score += sum(kw.lower() in (section_title or "").lower() for kw in IMPORTANCE_KEYWORDS)
    return score

def main():
    # Load input JSON
    with open("challenge1b_input.json", "r", encoding="utf-8") as f:
        inputs = json.load(f)

    persona = inputs["persona"]["role"]
    job_task = inputs["job_to_be_done"]["task"]

    # Load persona prompts
    with open("src/persona_prompts.json", "r", encoding="utf-8") as f:
        prompts = json.load(f)
    if persona not in prompts:
        print(f"Persona '{persona}' not found in persona_prompts.json! Supported: {list(prompts)}")
        sys.exit(1)

    base_prompt = prompts[persona]
    full_prompt = f"{base_prompt}\n\nTask: {job_task}"

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    extracted_sections = []
    subsection_analysis = []

    # For ranking (all sections with scores)
    ranked_sections = []

    for doc_entry in inputs["documents"]:
        filename = doc_entry["filename"]
        doc_path = os.path.join("data", filename)
        if not os.path.exists(doc_path):
            print(f"Document file not found: {doc_path}")
            continue
        print(f"Extracting sections from: {filename}")
        sections = extract_pdf_sections(doc_path)
        for sec in sections:
            # Use persona+task prompt to summarize this section
            section_summary = summarize_text(sec["section_text"], full_prompt)
            section_score = score_importance(sec["section_title"], section_summary, job_task)
            ranked_sections.append({
                "document": filename,
                "section_title": sec["section_title"],
                "page_number": sec["page_number"],
                "importance_rank": section_score,
                "refined_text": section_summary,
            })

    # Sort all sections by importance (higher score = more important, top 5 for extracted_sections as example)
    sorted_sections = sorted(ranked_sections, key=lambda x: -x["importance_rank"])
    extracted_sections = []
    for i, sec in enumerate(sorted_sections[:5]):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": i + 1,  # 1-based
            "page_number": sec["page_number"]
        })
    subsection_analysis = []
    for sec in sorted_sections[:10]:  # Up to 10 subsections in analysis (adjust as needed)
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": sec["refined_text"],
            "page_number": sec["page_number"]
        })

    # Compose output JSON exactly as sample
    output_json = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in inputs["documents"]],
            "persona": persona,
            "job_to_be_done": job_task,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    # Write output
    output_json_path = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, ensure_ascii=False, indent=2)

    print(f"\nStructured summaries and analysis saved in: {output_json_path}")

if __name__ == "__main__":
    main()
