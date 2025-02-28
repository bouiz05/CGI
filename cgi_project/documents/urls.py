from django.urls import path
from .views import DocumentViewSet

urlpatterns = [
    path('', DocumentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='documents'),

    path('<pk>/', DocumentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='document-detail'),

    path('<pk>/extract-names/', DocumentViewSet.as_view({
        'get': 'extract_names'
    }), name='document-extract-names'),
]
