# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer
from .services import extract_names_from_document

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def extract_names(self, request, pk=None):
        try:
            document = self.get_queryset().get(pk=pk)
        except Document.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        names = extract_names_from_document(document)
        return Response({"names": names}, status=status.HTTP_200_OK)
