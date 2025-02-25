# import requests
# from docx import Document

# # Step 1: Call Llama Parse API
# api_url = "https://api.llamaparser.com/parse"
# document_text = open("C:\\Users\\bouiz\\OneDrive\\Documents\\GitHub\\CGI\\cgi_project\\documents\\2.-Exemples-de-CV.pdf", "rb").read()


# response = requests.post(api_url, json={"text": document_text})
# parsed_data = response.json()  # Assume this returns structured data

# # Step 2: Process the parsed data (anonymization, replacement, etc.)
# def anonymize(text):
#     # This function would replace detected sensitive information with fictitious data.
#     # For demonstration, we're just returning the text unchanged.
#     return text

# processed_text = anonymize(parsed_data.get("content", ""))

# # Step 3: Create a new document with Python-docx
# doc = Document()
# doc.add_heading("Anonymized Document", 0)

# # For each paragraph in the processed text (you may need to split or structure the text accordingly)
# for para in processed_text.split("\n"):
#     doc.add_paragraph(para)

# # Optionally, modify styles and layout
# style = doc.styles['Normal']
# style.font.name = 'Arial'
# style.font.size = docx.shared.Pt(11)

# doc.save("output_document.docx")

import spacy
from pdfminer.high_level import extract_text as extract_text_pdf
from docx import Document as DocxDocument  
from .models import Document as DocumentModel
import io
from .anonymizer import process_document  # assuming you already have an anonymizer module

nlp = spacy.load("fr_core_news_sm")

def create_document(document_data):
    """
    Create and return a Document instance from the validated data.
    """
    document = DocumentModel.objects.create(**document_data)
    return document

def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_pdf(document_file):
    """
    Extract text from a PDF file and return it.
    """
    text = extract_text_from_pdf(document_file)
    return text

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

def extract_names_from_text(text):
    """
    Extract names from the text using spaCy and return them.
    """
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ in ['PER', 'PERSON']]
    return names

def extract_names_from_document(document_instance):
    """
    Extract names from the document and return them.
    """
    text = extract_text_from_pdf(document_instance.file.path)
    names = extract_names_from_text(text)
    return names

def anonymize_text(text, mapping):
    for original, replacement in mapping.items():
        text = text.replace(original, replacement)
    return text

def change_text_doc(text, output_path):
    doc = DocumentModel()
    doc.add_heading("Anonymized Document", 0)
    for para in text.split("\n"):
        doc.add_paragraph(para)
    doc.save(output_path)

def generate_docx(text):
    doc = DocxDocument()
    doc.add_heading("Anonymized Document", 0)
    for para in text.split("\n"):
        doc.add_paragraph(para)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

    