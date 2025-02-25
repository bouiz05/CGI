from django.apps import AppConfig


class ExtractionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'extraction'

    def ready(self):
        from .extractable_content_definitions import (
            STUDENTS_EXTRACTION
        )
        from .extractable_content_registry import ExtractableContentRegistry

        # Register all document types
        ExtractableContentRegistry.register(STUDENTS_EXTRACTION)
