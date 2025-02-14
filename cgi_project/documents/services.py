import spacy
from pdfminer.high_level import extract_text
from .models import Document
from .anonymizer import process_document  # assuming you already have an anonymizer module

nlp = spacy.load("fr_core_news_sm")

def create_document(document_data):
    """
    Create and return a Document instance from the validated data.
    """
    document = Document.objects.create(**document_data)
    return document

def extract_text_from_pdf(document_file):
    """
    Extract text from a PDF file and return it.
    """
    text = extract_text(document_file)
    return text

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