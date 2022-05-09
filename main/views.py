import base64
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from timer.models import UserLog
from calendarApp.form import TodoForm, TodoEditForm
from calendarApp.models import Todolist
from tag.models import Tag
from django.db.models import Q

import os, random
from withme.settings import MEDIA_ROOT

@csrf_exempt
def detectme(request):
    if request.POST:
        data = request.POST.__getitem__('data')
        data = data[22:] # data:image/png;base64 부분 제거
        number = random.randrange(1, 10000)

        # 저장 경로 및 파일명 설정
        filename = request.user.username + '_image_' + str(number) + '.png'
        save_path = os.path.join(MEDIA_ROOT, filename)

        image = open(save_path, "wb") # path+filename, "wb")
        image.write(base64.b64decode(data))
        image.close()

        # 모델 완성 시, 해당 result 반환
        number = random.randrange(1, 10000)
        user_state = '눈 뜨세요' if number % 2 else '화이팅 !!'
        answer = {
            'userState': user_state,
            'filepath' : save_path
            }

        return JsonResponse(answer)
    return render(request, 'main/video_test.html')


def pushmes(request):
    return render(request, 'main/pushmes_send.html')


@login_required
def camera_setting(request):
    item = UserLog.objects.filter(Q(user_id=request.user) & Q(end_time__isnull=True))
    if len(item) == 0:
        return render(request, 'main/camera_setting.html')
    else:
        item = item[0]
        todo_form = TodoForm()
        todo_list = Todolist.objects.all().filter(Q(author=request.user))
        tag = Tag.objects.get(pk=item.tag_id)

        return render(request, 'timer/service_main.html', {
            "todo_form": todo_form,
            "todo_edit_form": TodoEditForm,
            "todo_list": todo_list,
            "tag": tag,
            "user_log": item,
        })