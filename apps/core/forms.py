# In forms.py

from django import forms
from .models import Timeline

class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = ['event_title', 'event_description', 'date', 'time']
