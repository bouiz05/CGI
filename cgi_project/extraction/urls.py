from django.urls import path, include
from .views import *

urlpatterns = [
    path('extract/', DocumentExtractionView.as_view(), name='extract'),
]