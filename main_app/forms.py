from django.forms import ModelForm
from .models import Entry
from django.urls import reverse

class EntryForm(ModelForm):
    class Meta:
        model=Entry
        fields=["date","episode","season"]
        
    def get_absolute_url(self):
        return reverse('detail', kwargs={'content_id': self.id})