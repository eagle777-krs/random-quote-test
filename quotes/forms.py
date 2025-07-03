from django import forms
from .models import Quote, Source, Author

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя автора'})
        }

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название источника'}),
        }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Введите текст цитаты', 'rows': 4}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Приоритет цитаты'})
        }

class ExistingAuthorForm(forms.Form):
    existing_author = forms.ModelChoiceField(
        queryset=Author.objects.all().order_by('name'),
        required=False,
        label='Выбрать существующего автора',
        empty_label='Выберите автора или создайте нового'
    )

class ExistingSourceForm(forms.Form):
    existing_source = forms.ModelChoiceField(
        queryset=Source.objects.all().order_by('name'),
        required=False,
        label='Выбрать существующий источник',
        empty_label='Выберите источник или создайте новый'
    )