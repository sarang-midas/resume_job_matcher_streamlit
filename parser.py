import pdfplumber
import docx

def extract_text_from_pdf(file_path):
    text = ''
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + ' '
    except Exception:
        pass
    return text

def extract_text_from_docx(file_path):
    text = ''
    try:
        doc = docx.Document(file_path)
        for p in doc.paragraphs:
            if p.text:
                text += p.text + ' '
    except Exception:
        pass
    return text
