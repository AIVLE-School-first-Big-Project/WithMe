from django import forms
from .models import *

class timeForm(forms.ModelForm):
  class Meta:
    model = User_log

    fields = ['tag_name','start_time','pause','end_time','abnomal_time']  # id 속성은 PK 이므로 사용하지 않음

    labels = {  # 오류 메시지에 보여줄 단어
        
        'tag_name': '과목이름',
        'start_time':'시작 시간',
        'pause': '일시정지',
        'end_time': '종료 시간',
        'abnormal_time': '이상시간'
    }