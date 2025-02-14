import os
from pdfminer.high_level import extract_text
import spacy

# Load an NLP model, for instance, spaCy's French model
nlp = spacy.load("fr_core_news_sm")

def anonymize_text(text):
    """
    Replace sensitive entities in text with fake placeholders.
    Returns the anonymized text along with a mapping of original values to placeholders.
    """
    doc = nlp(text)
    mapping = {}
    anonymized_text = text

    # For demonstration, we target entities like PERSON and GPE
    for ent in doc.ents:
        if ent.label_ in ['PER', 'PERSON', 'GPE', 'LOC']:
            if ent.text not in mapping:
                fake_value = f"<fake_{ent.label_}_{len(mapping)+1}>"
                mapping[ent.text] = fake_value
            anonymized_text = anonymized_text.replace(ent.text, mapping[ent.text])
    return anonymized_text, mapping

def process_document(document_instance):
    """
    Process the uploaded document:
      1. Extract text from the document.
      2. Anonymize the text.
      3. Save the anonymized text to a new file.
      4. Update the document instance with the anonymized file path, mapping, and status.
    """
    # Extract text from the original file
    file_path = document_instance.file.path
    text = extract_text(file_path)

    # Anonymize the extracted text
    anonymized_text, mapping = anonymize_text(text)

    # Define where to save the anonymized file (for this demo, we save it as a .txt file)
    base_dir = os.path.dirname(file_path)
    anonymized_dir = base_dir.replace('documents', 'anonymized')
    if not os.path.exists(anonymized_dir):
        os.makedirs(anonymized_dir)
    anonymized_file_path = os.path.join(anonymized_dir, os.path.basename(file_path) + '.txt')

    # Write the anonymized text to a file
    with open(anonymized_file_path, 'w', encoding='utf-8') as f:
        f.write(anonymized_text)

    # Update the Document instance with relative path, mapping, and status
    relative_path = anonymized_file_path.split('media' + os.sep)[-1]
    document_instance.anonymized_file.name = relative_path
    document_instance.mapping = mapping
    document_instance.status = 'processed'
    document_instance.save()

    return mapping
