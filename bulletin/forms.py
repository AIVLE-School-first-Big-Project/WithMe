from .models import BulletinFeed
from django import forms

# 글쓰기 기능 관련 폼 추가
class BulletinFeedForm(forms.ModelForm):
    class Meta:
        model = BulletinFeed
        fields = ['title', 'content']
        
        labels = {'title': '제목','content': '내용',}