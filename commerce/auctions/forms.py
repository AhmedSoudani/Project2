from .models import listing, bids
from django import forms

class listingform(forms.ModelForm):
    class Meta :
        model = listing
        fields = ['title', 'description', 'price', 'image_URL']

class BidForm(forms.ModelForm):
    class Meta:
        model = bids
        fields = ['bid_price']
        widgets = {
            'bid_amount': forms.TextInput(attrs={'placeholder': 'Enter bid...'}),
        }