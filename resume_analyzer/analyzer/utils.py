import fitz  # PyMuPDF for PDF extraction
import docx

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file"""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    except Exception as e:
        return f"Error reading PDF: {e}"
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file"""
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        return f"Error reading DOCX: {e}"
    return text
