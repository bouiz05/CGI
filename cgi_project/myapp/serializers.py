from rest_framework import serializers
from .models import TestModel

from .services import create_test_model

class TestModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = '__all__'

    def create(self, validated_data):
        return create_test_model(validated_data)