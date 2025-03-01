from rest_framework import serializers
from .models import Document
from .services import create_document, extract_names_from_document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def create(self, validated_data):
        return create_document(validated_data)
    
class ExtractNamesSerializer(serializers.ModelSerializer):
    names = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'names')

    def get_names(self, obj):
        return extract_names_from_document(obj)