from docx import Document
from PyPDF2 import PdfReader

def load_jobdesc(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        text = "".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".docx"):
        doc = Document(file)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        text = file.read().decode("utf-8")
    return text.strip()
