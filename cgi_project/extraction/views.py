from rest_framework.response import Response
from .file_parser import FileParser
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import DocumentExtractionSerializer
from .extractable_content_registry import ExtractableContentRegistry
from openai import OpenAI
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from .extraction_strategy import LlamaParseStrategy

class DocumentExtractionView(GenericAPIView):
    serializer_class = DocumentExtractionSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        type = serializer.validated_data['type']

        # TODO: this is a service logic and should be moved to the freaking service
        extraction_strategy = LlamaParseStrategy()

        try:
            output = extraction_strategy.extract(file, ExtractableContentRegistry.get(type))

            return Response(output.model_dump(), status=200)
        except Exception as e:
            return Response(str(e), status=500)
            
