# from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject

# def fill_pdf(input_pdf_path, output_pdf_path, data):
#     pdf = PdfReader(input_pdf_path)
    
#     # Force the PDF to display filled fields
#     if "/AcroForm" in pdf.Root:
#         pdf.Root.AcroForm.update(
#             PdfDict(NeedAppearances=PdfObject("true"))
#         )
#     else:
#         pdf.Root.AcroForm = PdfDict(NeedAppearances=PdfObject("true"))

#     for page in pdf.pages:
#         annotations = page.Annots
#         if annotations:
#             for annot in annotations:
#                 if annot.Subtype == PdfName.Widget and annot.T:
#                     key = annot.T.to_unicode().strip("()")
#                     if key in data:
#                         annot.V = PdfObject(f"({data[key]})")
#                         annot.AP = ''
#                         annot.AS = ''
    
#     PdfWriter().write(output_pdf_path, pdf)
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfObject

def fill_pdf(template_path, output_path, data_dict, checkboxes=None):
    # 1) Read the PDF
    pdf = PdfReader(template_path)

    # 2) Force the PDF to render the fields
    pdf.Root.AcroForm.update(
        PdfDict(NeedAppearances=PdfObject("true"))
    )

    # 3) Loop over all pages & annotations
    for page in pdf.pages:
        if not page.Annots:
            continue

        for annot in page.Annots:
            # Only deal with actual form fields
            if annot.Subtype == PdfName.Widget and annot.T:
                # E.g. "(CheckBoxBattery)" → "CheckBoxBattery"
                key = annot.T.to_unicode().strip("()")

                ############################################################
                # A) If this key is in data_dict, fill it as text
                ############################################################
                if key in data_dict:
                    annot.V = PdfObject(f"({data_dict[key]})")
                    annot.AP = ''
                    annot.AS = ''

                ############################################################
                # B) If this key is in checkboxes, we want to check it
                ############################################################
                elif checkboxes and key in checkboxes and checkboxes[key]:
                    # The user wants this box checked (True)
                    # So let's detect the PDF's real "on" value.

                    # /AP is the appearance dictionary
                    # /N is the "normal" appearance states
                    ap_dict = annot.get("/AP", {}).get("/N", {})
                    # We skip "/Off"
                    on_candidates = [
                        k for k in ap_dict.keys()
                        if k not in (PdfName.Off, PdfName("Off"))
                    ]

                    if on_candidates:
                        on_val = on_candidates[0]  # e.g. /On, /Yes, /1
                    else:
                        # fallback if none found
                        on_val = PdfName.Yes

                    annot.update(
                        PdfDict(
                            V=on_val,
                            AS=on_val
                        )
                    )

                ############################################################
                # C) Otherwise do nothing
                ############################################################

    # 4) Write out the result
    PdfWriter().write(output_path, pdf)



