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


# class DocumentAnonymizationSerializer(serializers.ModelSerializer):
#     """
#     This serializer could be used if you want to trigger the anonymization
#     process via an API endpoint. It doesn't really create a new model instance,
#     but rather calls the anonymization service.
#     """
#     class Meta:
#         model = Document
#         fields = ('id',)  # or any other fields you want to include

#     def create(self, validated_data):
#         document = Document.objects.get(pk=validated_data.get('id'))
#         mapping = anonymize_document(document)
#         return document
