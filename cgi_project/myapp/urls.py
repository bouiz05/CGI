from django.urls import path
from .views import TestModelViewSet

urlpatterns = [
    path('test/', TestModelViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='test'),
]