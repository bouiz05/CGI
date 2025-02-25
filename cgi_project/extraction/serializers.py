from rest_framework import serializers
from .extractable_content_registry import ExtractableContentRegistry

class DocumentExtractionSerializer(serializers.Serializer):
    file = serializers.FileField()
    type = serializers.CharField()

    def validate_type(self, value):
        try:
            ExtractableContentRegistry.get(value)
        except ValueError:
            raise serializers.ValidationError("Unknown file type")
        return value
    
    def validate_file(self, value):
        supported_extensions = ('.pdf', '.png', '.jpg', '.jpeg')

        if not value.name.endswith(supported_extensions):
            raise serializers.ValidationError("Unsupported file format")
        
        if value.size > 1024 * 1024:
            raise serializers.ValidationError("File size exceeds 1MB")

        return value
    