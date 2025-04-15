# from modules.audio_processor import transcribe_audio
# from modules.nlp_extractor import extract_data
# from pdfrw import PdfReader, PdfWriter, PdfDict

# def fill_pdf(input_pdf_path, output_pdf_path, data):
#     template_pdf = PdfReader(input_pdf_path)
#     template_pdf.Root.AcroForm.update(PdfDict(NeedAppearances=PdfDict(indirect=True)))
#     for page in template_pdf.pages:
#         annotations = page.Annots
#         if annotations:
#             for annot in annotations:
#                 if annot.Subtype == '/Widget' and annot.T:
#                     key = annot.T[1:-1]
#                     if key in data:
#                         annot.V = f"({data[key]})"
#                         annot.AP = ''
#                         annot.AS = ''
#     PdfWriter().write(output_pdf_path, template_pdf)

# # === RUNNING THE PIPELINE ===
# audio_path = "sample_audio.mp3"
# pdf_template = "sample_fillable_form.pdf"
# output_path = "filled_sample_output.pdf"

# transcript = transcribe_audio(audio_path)
# print("Transcript:", transcript)

# data = extract_data(transcript)
# print("Extracted:", data)

# fill_pdf(pdf_template, output_path, data)
# print(f"✅ PDF filled and saved to: {output_path}")


from modules.audio_processor import transcribe_audio
from modules.nlp_extractor import extract_data
from modules.template_matcher import match_template
from modules.word_filler import fill_word_template  # ← NEW

# Assume your audio and template paths are already defined
audio_path = "sample_audio.mp3"
template_path = "fitting_followup_template.docx"
output_path = "filled_followup.docx"

# 1. Transcribe audio
transcript = transcribe_audio(audio_path)

# 2. Extract text fields and checkbox states
extracted, checkboxes = extract_data(transcript)  # Make sure this returns two dicts

# 3. Merge and fill Word template
data_to_fill = {**extracted, **checkboxes}
fill_word_template(template_path, output_path, data_to_fill)

print(f"\n✅ Done! Word document generated: {output_path}")



