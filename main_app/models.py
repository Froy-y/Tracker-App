from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class Content(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    seasons = models.IntegerField()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'content_id': self.id})
    
    def entry_for_today(self):
        return self.entry_set.filter(date=date.today()).count()
    
class Entry(models.Model):
    date = models.DateField('Entry Date')
    episode = models.IntegerField(default=1)
    season = models.IntegerField(default=1)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Watched Episode {self.get_episode_display()} Season {self.get_season_display()} on {self.date}"
    
    class Meta:
        ordering = ['-date']