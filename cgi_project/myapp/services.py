from .models import TestModel

def create_test_model(test_data):
    test_model = TestModel.objects.create(**test_data)
    return test_model