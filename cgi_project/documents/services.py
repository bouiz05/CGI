import spacy
from pdfminer.high_level import extract_text
from .models import Document
from .anonymizer import process_document
import re
import pyap
import chardet
from docx import Document as DocxDocument


SPACY_MODEL = "fr_core_news_sm"

EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
PHONE_FR_REGEX = r"(?:\+1\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"


def detect_addresses(text):
    addresses = pyap.parse(text, country="CA")  
    detected_addresses = []

    for address in addresses:
        street = f"{address.street_number} {address.street_name}"
        city = address.city
        state = address.region1
        postal_code = address.postal_code
        country = address.country_id

        full_address = f"{street}, {city}, {state} {postal_code}, {country}"
        detected_addresses.append(full_address)

    return detected_addresses

def is_full_name(text):
    parts = text.split()
    return len(parts) >= 2 and all(any(c.isalpha() for c in part) for part in parts)

def load_spacy_model(model_name=SPACY_MODEL):
    try:
        return spacy.load(model_name)
    except OSError:
        logger.info(f"Downloading spaCy model '{model_name}'...")
        from spacy.cli import download
        download(model_name)
        return spacy.load(model_name)

nlp = load_spacy_model()

def create_document(document_data):
    document = Document.objects.create(**document_data)
    return document

def extract_text_from_pdf(pdf_path):
    try:
        raw_text = extract_text(pdf_path)
        encoding = chardet.detect(raw_text.encode())['encoding']
        text = raw_text.encode(encoding).decode('utf-8')
        return text
    except Exception as e:
        print(f"Erreur avec pdfminer : {e}")
        return None

def extract_text_from_docx(docx_path):
    doc = DocxDocument(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def extract_names_from_text(text):
    doc=nlp(text)
    names = [
        ent.text.strip() 
        for ent in doc.ents 
        if ent.label_ in ['PER', 'PERSON'] and is_full_name(ent.text)
        ]
    
    emails = re.findall(EMAIL_REGEX, text)
    
    phones = re.findall(PHONE_FR_REGEX, text)
    
    addresses = detect_addresses(text)
    
    return {
        "names": list(set(names)),
        "emails": list(set(emails)),
        "phones": [re.sub(r'\D', '', p) for p in phones],
        "addresses": list(set(addresses))
    }

def extract_text_from_file(file_path):
    extension = file_path.lower().split('.')[-1]
    if extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif extension == 'docx':
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {extension}")

def extract_names_from_document(document_instance):
    try:
        text = extract_text_from_file(document_instance.file.path)
        return extract_names_from_text(text)
    except Exception as e:
        print(f"Error processing document: {e}")
        return {
            "names": [],
            "emails": [],
            "phones": [],
            "addresses": [],
        }
