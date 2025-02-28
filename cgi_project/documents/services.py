import spacy
from pdfminer.high_level import extract_text
from .models import Document
from .anonymizer import process_document
import re
import pyap
import chardet


# Liste des modèles spaCy requis
SPACY_MODEL = "fr_core_news_sm"

# Expressions régulières
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
PHONE_FR_REGEX = r"(?:\+1\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"


def detect_addresses(text):
    # Détection des adresses avec pyap
    addresses = pyap.parse(text, country="CA")  # 'CA' pour le Canada

    # Liste pour stocker les adresses détectées
    detected_addresses = []

    for address in addresses:
        # Extraire les composants de l'adresse
        street = f"{address.street_number} {address.street_name}"
        city = address.city
        state = address.region1
        postal_code = address.postal_code
        country = address.country_id

        # Formater l'adresse complète
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

# Load spaCy model
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

def extract_names_from_text(text):
    """Extrait les noms, emails, téléphones et adresses d'un texte."""
    doc=nlp(text)
    names = [
        ent.text.strip() 
        for ent in doc.ents 
        if ent.label_ in ['PER', 'PERSON'] and is_full_name(ent.text)
        ]
    
    # Détection des emails
    emails = re.findall(EMAIL_REGEX, text)
    
    # Détection des numéros FR
    phones = re.findall(PHONE_FR_REGEX, text)
    
    # Détection des adresses
    addresses = detect_addresses(text)
    
    return {
        "names": list(set(names)),
        "emails": list(set(emails)),
        "phones": [re.sub(r'\D', '', p) for p in phones],
        "addresses": list(set(addresses))
    }

def extract_names_from_document(document_instance):
    """Extrait les informations d'un document PDF avec gestion d'erreurs."""
    try:
        # Extraction du texte depuis le PDF
        text = extract_text_from_pdf(document_instance.file.path)
        # Extraction des informations
        return extract_names_from_text(text)
    except Exception as e:
        print(f"Erreur lors du traitement du document: {e}")
        return {
            "names": [],
            "emails": [],
            "phones": [],
            "addresses": [],
        }