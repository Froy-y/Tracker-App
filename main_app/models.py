from django.db import models

# Create your models here.
class Content(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    seasons = models.IntegerField()
    
    def __str__(self):
        return self.name