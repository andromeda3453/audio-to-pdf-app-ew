from PyPDF2 import PdfReader

reader = PdfReader("templates/sample_fillable_form.pdf")
fields = set()
for page in reader.pages:
    if "/Annots" in page:
        for annot in page["/Annots"]:
            field = annot.get_object()
            name = field.get("/T")
            if name:
                fields.add(name)

print("Field names in the PDF:")
for f in fields:
    print(f)
