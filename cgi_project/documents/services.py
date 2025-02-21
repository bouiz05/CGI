import spacy
from pdfminer.high_level import extract_text
from .models import Document
from .anonymizer import process_document
import re

# Liste des modèles spaCy requis
SPACY_MODELS = ["en_core_web_sm", "fr_core_news_sm"]
# Expressions régulières
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
PHONE_FR_REGEX = r"(?:\+1\s?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"

# Fonction de validation
def is_full_name(text):
    parts = text.split()
    return len(parts) >= 2 and all(any(c.isalpha() for c in part) for part in parts)


def load_spacy_model(model_name):

    try:
        return spacy.load(model_name)
    except OSError:
        print(f"Téléchargement du modèle spaCy '{model_name}'...")
        from spacy.cli import download
        download(model_name)
        return spacy.load(model_name)

# Chargement de tous les modèles choisies
for i in SPACY_MODELS:
    nlp = load_spacy_model(i)

def create_document(document_data):
    document = Document.objects.create(**document_data)
    return document

def extract_text_from_pdf(document_file):
    return extract_text(document_file)

def extract_names_from_text(text):
    # Utilisation combinée des modèles
    names = []
    for lang, nlp in nlp_models.items():
        doc = nlp(text)
        names += [
            ent.text.strip() 
            for ent in doc.ents 
            if ent.label_ in ['PER', 'PERSON'] and is_full_name(ent.text)
        ]
    
    # Détection manuelle des noms en capitale
    for word in text.split():
        if word.istitle() and is_full_name(word) and word not in names:
            names.append(word)    
    # Détection des entités
    doc = nlp(text)
    names = [
        ent.text.strip() 
        for ent in doc.ents 
        if ent.label_ in ['PER', 'PERSON'] and is_full_name(ent.text)
    ]
    
    # Détection des emails
    emails = re.findall(EMAIL_REGEX, text)
    
    # Détection des numéros FR
    phones = re.findall(PHONE_FR_REGEX, text)
    
    return {
        "names": list(set(names)),
        "emails": list(set(emails)),
        "phones": [re.sub(r'\D', '', p) for p in phones],
        "adress": []#TODO: adresse

    }

def extract_names_from_text(text):
    """Version améliorée avec détection des emails/numéros"""
    # Détection des entités
    doc = nlp(text)
    names = [
        ent.text.strip() 
        for ent in doc.ents 
        if ent.label_ in ['PER', 'PERSON'] and is_full_name(ent.text)
    ]
    
    # Détection des emails
    emails = re.findall(EMAIL_REGEX, text)
    
    # Détection des numéros FR
    phones = re.findall(PHONE_FR_REGEX, text)
    
    return {
        "names": list(set(names)),
        "emails": list(set(emails)),
        "phones": [re.sub(r'\D', '', p) for p in phones],
        "adress": []#TODO: adresse
    }

def extract_names_from_document(document_instance):
    """Version améliorée avec gestion d'erreurs"""
    try:
        text = extract_text_from_pdf(document_instance.file.path)
        return extract_names_from_text(text)
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        return {
            "names": [],
            "emails": [],
            "phones": [],
            "adress": []#TODO: adresse

        }
