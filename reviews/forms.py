from random import choices

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Scrivi la tua recensione'}),
            'rating': forms.RadioSelect(attrs={'class': 'form-check-input'}, choices=[(i, f"{i}stelle") for i in range(1, 6)]),
        }