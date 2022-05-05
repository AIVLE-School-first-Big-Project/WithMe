from django import forms
from .models import Todolist
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class TodoForm(forms.ModelForm):
  class Meta:
    model = Todolist
    fields = ['description', 'date_to']
    labels = {
      'description': '내용',
      'date_to': '마감일',
    }
    widgets = {
      'date_to': DateTimePickerInput(),
    }

class TodoEditForm(forms.ModelForm):
  class Meta:
    model = Todolist
    fields = ['confirm', 'description', 'date_to']
    labels = {
      'confirm': '완료',
      'description': '내용',
      'date_to': '마감일',
    }
    widgets = {
      'date_to': DateTimePickerInput(),
    }