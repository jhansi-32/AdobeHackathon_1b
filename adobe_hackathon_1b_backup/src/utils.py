import os
import pdfplumber
import re

def extract_pdf_sections(filepath):
    """
    Extracts sections from a PDF, returning a list of dicts:
    [{'section_title': ..., 'section_text': ..., 'page_number': ...}]
    Section detection: based on headings (lines in ALL CAPS, bold, or pattern).
    """
    sections = []
    last_section = None
    last_title = None
    page_num = 1

    # Pattern for what looks like a heading (ALL CAPS or Title Case, flexible)
    heading_pattern = re.compile(r'^([A-Z][A-Z\s\-:&\']{6,}|([A-Z][a-z]+ ){1,4}[A-Z][a-z]+)$')

    with pdfplumber.open(filepath) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = text.split('\n')
            cur_section_text = []
            cur_section_title = None
            for line in lines:
                striped = line.strip()
                # Is this line a heading?
                if heading_pattern.match(striped) and len(striped.split()) <= 10:
                    # Save previous section if non-empty
                    if cur_section_title and cur_section_text:
                        sections.append({
                            "section_title": cur_section_title,
                            "section_text": "\n".join(cur_section_text).strip(),
                            "page_number": i + 1
                        })
                        cur_section_text = []
                    cur_section_title = striped
                else:
                    cur_section_text.append(striped)
            # End of page: save last section on this page
            if cur_section_title and cur_section_text:
                sections.append({
                    "section_title": cur_section_title,
                    "section_text": "\n".join(cur_section_text).strip(),
                    "page_number": i + 1
                })
    # Filter: only return sections with non-empty text and titles
    return [s for s in sections if len(s.get("section_text", "")) > 40 and s.get("section_title")]
