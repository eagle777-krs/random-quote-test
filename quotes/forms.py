# forms.py

from django import forms
from .models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'weight', 'source']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Текст цитаты'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Вес'}),
            'source': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].required = True  # источник обязателен


class QuoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'weight', 'source']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Текст цитаты'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Вес'}),
            'source': forms.Select()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['source'].required = True
