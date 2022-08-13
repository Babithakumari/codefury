# forms.py
from django import forms
from .models import *
  
class StartupForm(forms.ModelForm):
  
    class Meta:
        model = Startup
        fields = ['name', 'hotel_Main_Img']