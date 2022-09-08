from django.db import models

# Create your models here.
  
class Coin(models.Model):
    name = models.CharField(max_length=255)
    hash = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    marketcap = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    volume = models.CharField(max_length=255)
    percent = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name