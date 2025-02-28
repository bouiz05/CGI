from django.test import TestCase
from unittest.mock import patch, MagicMock
from .services import (
    detect_addresses,
    is_full_name,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_names_from_text,
    extract_names_from_document,
)
import re
import pyap
from .models import Document
import os

class ServiceTests(TestCase):
    
    def test_is_full_name(self):
        self.assertTrue(is_full_name("John Doe"))
        self.assertTrue(is_full_name("Jean-Luc Picard"))
        self.assertFalse(is_full_name("John"))
        self.assertFalse(is_full_name("12345"))
    

    def test_detect_addresses(self):
        sample_text = "Mon adresse est 123 Main St, Toronto, ON M5V 3A8, CA."
        addresses = detect_addresses(sample_text)
        self.assertIn("123 Main, Toronto, ON M5V 3A8, CA", addresses)

    def test_empty_string(self):
        text = ""
        result = extract_names_from_text(text)
        self.assertEqual(result["names"], [])
        self.assertEqual(result["emails"], [])
        self.assertEqual(result["phones"], [])
        self.assertEqual(result["addresses"], [])

    def test_extract_text_from_docx(self):
        text = extract_text_from_docx("documents\pdf\CV_2025_1.docx")
        self.assertIsNotNone(text)
        self.assertIn("Bouezmarni Mohamed", text)
        self.assertIn("mohamed.bouezmarni.1@ulaval.ca", text)
    

    def test_extract_text_from_pdf(self):
        text = extract_text_from_pdf("documents\pdf\CV_English_Mostafa_V3_aecO2O2.pdf")
        self.assertIsNotNone(text)
        self.assertIn("MOSTAFA FILALI", text)
        