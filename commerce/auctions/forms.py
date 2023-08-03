from .models import listing
from django import forms

class listingform(forms.ModelForm):
    class Meta :
        model = listing
        fields = ['title', 'description', 'price', 'image_URL']