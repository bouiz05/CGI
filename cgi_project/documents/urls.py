# urls.py
from django.urls import path
from .views import DocumentViewSet

urlpatterns = [
    # List and Create
    path('', DocumentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='documents'),

    # Retrieve, Update, Delete
    path('<pk>/', DocumentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='document-detail'),

    # Custom action for name extraction
    path('<pk>/extract-names/', DocumentViewSet.as_view({
        'get': 'extract_names'
    }), name='document-extract-names'),

    path('<pk>/download-anonymized/', DocumentViewSet.as_view({
        'get': 'download_anonymized'
    }), name='document-download-anonymized'),
]
