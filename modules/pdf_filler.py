from pdfrw import PdfReader, PdfWriter, PdfDict

def fill_pdf(template_path: str, output_path: str, data_dict: dict):
    """
    Fills a PDF form template with data from `data_dict`.
    data_dict keys must match the PDF form field /T values.
    """
    pdf = PdfReader(template_path)
    for page in pdf.pages:
        annotations = page.get("/Annots")
        if annotations:
            for annotation in annotations:
                if annotation.get("/Subtype") == "/Widget" and annotation.get("/T"):
                    field_key = annotation["/T"][1:-1]  # strip parentheses
                    if field_key in data_dict:
                        annotation.update(PdfDict(V=str(data_dict[field_key])))

    PdfWriter(output_path, trailer=pdf).write()
