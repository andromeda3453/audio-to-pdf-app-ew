# import spacy
# import re

# nlp = spacy.load("en_core_web_sm")

# def extract_data(text: str) -> dict:
#     """
#     Extracts relevant data with spaCy (or regex).
#     Returns a dict that matches PDF form field names.
#     """
#     doc = nlp(text)
#     data = {}

#     # Example: pick up the first recognized PERSON or DATE
#     for ent in doc.ents:
#         if ent.label_ == "PERSON":
#             data["Name"] = ent.text
#             print(ent.text)
#         elif ent.label_ == "DATE":
#             data["Date"] = ent.text
#             print(ent.text)


#     # Example: phone number via naive regex
#     phone_match = re.search(r"(\+?\d{1,2}\s?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}", text)

#     if phone_match:
#         data["Phone"] = phone_match.group(0)  

#     return data

def extract_data(text: str) -> tuple:
    extracted = {}
    checkboxes = {}
    text_lower = text.lower()

    # --- Text Fields ---
    import re

    # Audiologist name
    aud_match = re.search(r"my name is\s+(.+?)(?:[.,]|$)", text, re.IGNORECASE)
    if aud_match:
        extracted["AUDIOLOGIST"] = aud_match.group(1).strip()

    # Follow up date
    fud_match = re.search(r"date of follow[- ]?up is\s+(.+?)(?:[.,]|$)", text, re.IGNORECASE)
    if fud_match:
        extracted["FOLLOW_UP_DATE"] = fud_match.group(1).strip()

    # Provider Number
    provider_match = re.search(r"provider number is\s+(.+?)(?:[.,]|$)", text, re.IGNORECASE)
    if provider_match:
        extracted["PROVIDER_NUMBER"] = provider_match.group(1).strip()

    # Patient Name
    patient_match = re.search(r"patient'?s name is\s+(.+?)(?:[.,]|$)", text, re.IGNORECASE)
    if patient_match:
        extracted["PATIENT_NAME"] = patient_match.group(1).strip()

    # DOB
    dob_match = re.search(r"date of birth is\s+(.+?)(?:[.,]|$)", text, re.IGNORECASE)
    if dob_match:
        extracted["DOB"] = dob_match.group(1).strip()

    # Referring Physician
    ref_match = re.search(r"referred by\s+(.+?)(?:[.,]|$)", text, re.IGNORECASE)
    if ref_match:
        extracted["REFERRING_PHYSICIAN"] = ref_match.group(1).strip()

    # --- Checkboxes ---
    checkboxes["CHECKBOX_PRIVATE"] = "[X]" if "private fitting" in text_lower else "[ ]"
    checkboxes["CHECKBOX_HSP_QUOTE"] = "[X]" if "hsp has been signed" in text_lower else "[ ]"
    checkboxes["CHECKBOX_TARGETS_MET"] = "[X]" if "targets were met" in text_lower else "[ ]"
    checkboxes["CHECKBOX_BATTERY"] = "[X]" if "battery" in text_lower else "[ ]"
    checkboxes["CHECKBOX_CLEANING"] = "[X]" if "cleaning" in text_lower else "[ ]"
    checkboxes["CHECKBOX_EDUCATION"] = "[X]" if "education" in text_lower else "[ ]"
    checkboxes["CHECKBOX_COMMUNICATION"] = "[X]" if "communication" in text_lower else "[ ]"
    checkboxes["CHECKBOX_FUTURE_RECALL"] = "[X]" if "future recall" in text_lower else "[ ]"

    # Optional default values
    extracted["APPOINTMENT_NOTES"] = "Auto-filled from audio transcript."

    return extracted, checkboxes


