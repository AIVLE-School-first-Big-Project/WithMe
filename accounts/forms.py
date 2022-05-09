from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django import forms
from .models import User


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "비밀번호나 이름이 올바르지 않습니다."
        )
    }

    def __init__(self, request=None, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = '__Name'
        self.fields["username"].widget.attrs.update({
            'class': 'bg-transparent text-white border-white',
        })
        self.fields['password'].label = '__Password'
        self.fields["password"].widget.attrs.update({
            'class': 'bg-transparent text-white border-white',
        })


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['User_type']


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class': 'bg-transparent text-white border-white',
        })
        self.fields["password1"].widget.attrs.update({
            'class': 'bg-transparent text-white border-white',
        })
        self.fields["password2"].widget.attrs.update({
            'class': 'bg-transparent text-white border-white',
        })
        self.fields["User_type"].widget.attrs.update({
            'class': 'bg-transparent text-white border-white',
        })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'User_type']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 아이디입니다.")
        return username


