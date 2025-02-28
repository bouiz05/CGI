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

class ServiceTests(TestCase):
    def test_is_full_name(self):
        """Teste si la fonction is_full_name identifie correctement les noms complets."""
        self.assertTrue(is_full_name("John Doe"))
        self.assertTrue(is_full_name("Jean-Luc Picard"))
        self.assertFalse(is_full_name("John"))
        self.assertFalse(is_full_name("12345"))