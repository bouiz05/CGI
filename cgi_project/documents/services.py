import spacy
from pdfminer.high_level import extract_text
from .models import Document
from .anonymizer import process_document

# Liste des modèles spaCy requis
SPACY_MODELS = ["en_core_web_sm", "fr_core_news_sm"]

def load_spacy_model(model_name):
    """Charge un modèle spaCy en le téléchargeant si nécessaire"""
    try:
        return spacy.load(model_name)
    except OSError:
        print(f"Téléchargement du modèle spaCy '{model_name}'...")
        from spacy.cli import download
        download(model_name)
        return spacy.load(model_name)

# Chargement du modèle principal (ajuster selon vos besoins)
nlp = load_spacy_model(SPACY_MODELS[0])

def create_document(document_data):
    """Crée et retourne une instance Document à partir des données validées"""
    document = Document.objects.create(**document_data)
    return document

def extract_text_from_pdf(document_file):
    """Extrait le texte d'un fichier PDF et le retourne"""
    return extract_text(document_file)

def extract_names_from_text(text):
    """Extrait les noms du texte avec spaCy"""
    doc = nlp(text)
    return [ent.text for ent in doc.ents if ent.label_ in ['PER', 'PERSON']]

def extract_names_from_document(document_instance):
    """Extrait les noms d'un document"""
    text = extract_text_from_pdf(document_instance.file.path)
    return extract_names_from_text(text)