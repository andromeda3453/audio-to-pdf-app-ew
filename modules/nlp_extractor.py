import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_data(text: str) -> dict:
    """
    Extracts relevant data with spaCy (or regex).
    Returns a dict that matches PDF form field names.
    """
    doc = nlp(text)
    data = {}

    # Example: pick up the first recognized PERSON or DATE
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            data["Name"] = ent.text
        elif ent.label_ == "DATE":
            data["Date"] = ent.text

    # Example: phone number via naive regex
    phone_match = re.search(r"(\+?\d{1,2}\s?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}", text)

    if phone_match:
        data["Phone"] = phone_match.group(0)

    return data
