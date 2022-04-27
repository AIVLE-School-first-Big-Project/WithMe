from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['User_type']


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'User_type']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 아이디입니다.")
        return username


