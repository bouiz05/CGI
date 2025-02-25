# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer
from .services import extract_names_from_document, extract_text_from_pdf, anonymize_text, generate_docx

class DocumentViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - CRUD for Document model
    - A custom method 'extract_names'
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def extract_names(self, request, pk=None):
        """
        Custom method to extract names from the Document at <pk>.
        Called via GET /documents/<pk>/extract-names/
        """
        try:
            document = self.get_queryset().get(pk=pk)
        except Document.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        names = extract_names_from_document(document)
        return Response({"names": names}, status=status.HTTP_200_OK)
    
    def download_anonymized(self, request, pk=None):
        """
        Custom action to extract text, anonymize it, generate a DOCX file, and return it.
        Endpoint: GET /documents/<pk>/download-anonymized/
        """
        try:
            document = self.get_queryset().get(pk=pk)
        except Document.DoesNotExist:
            return Response({"detail": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Extract text from the document (assuming it's a PDF; adjust as needed)
        text = extract_text_from_pdf(document.file.path)
        
        # Create a mapping for anonymization (you can adjust this to your needs)
        mapping = {
            "Mohamed Bouezmarni": "REDACTED_NAME",  # example mapping
            # add more mappings or use your anonymizer logic
        }
        anonymized_text = anonymize_text(text, mapping)
        
        # Generate the DOCX file in memory
        file_buffer = generate_docx(anonymized_text)
        
        # Create an HTTP response with the appropriate headers for downloading a DOCX file
        response = HttpResponse(
            file_buffer.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        response["Content-Disposition"] = 'attachment; filename="anonymized_document.docx"'
        return response
