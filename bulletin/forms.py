from .models import Post
from django import forms


# 글쓰기 기능 관련 폼 추가
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

        labels = {'title': '제목', 'content': '내용', 'image': '사진'}
