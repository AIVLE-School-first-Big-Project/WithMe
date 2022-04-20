from dal import autocomplete

from django import forms

from .models import Tag


class TForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('Tag_name')
        widgets = {
            'Tag_name': autocomplete.ModelSelect2(url='test')
        }