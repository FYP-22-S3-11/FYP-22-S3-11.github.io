from django.db import models

# Create your models here.
  
class Crypto(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
  
    def __str__(self) -> str:
        return self.name