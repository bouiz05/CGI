from django.db import models

# Create your models here.

class TestModel(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return self.name
