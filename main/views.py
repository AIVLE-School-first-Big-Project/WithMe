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
from timer.models import UserLog
from tag.models import Tag
import os, random
from withme.settings import MEDIA_ROOT
from django.utils.dateparse import parse_datetime
import datetime


@csrf_exempt
def detectme(request):
    if request.POST:
        data = request.POST.__getitem__('data')
        data = data[22:]  # data:image/png;base64 부분 제거
        number = random.randrange(1, 10000)

        # 저장 경로 및 파일명 설정
        filename = request.user.username + '_image_' + str(number) + '.png'
        save_path = os.path.join(MEDIA_ROOT, filename)

        image = open(save_path, "wb")  # path+filename, "wb")
        image.write(base64.b64decode(data))
        image.close()

        # 모델 완성 시, 해당 result 반환
        number = random.randrange(1, 10000)
        user_state = '눈 뜨세요' if number % 2 else '화이팅 !!'
        answer = {
            'userState': user_state,
            'filepath': save_path
        }

        return JsonResponse(answer)
    return render(request, 'main/video_test.html')


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


def get_month_data(user, date_str):
    userlog_items = UserLog.objects.filter(end_time__year=date_str[:4], end_time__month=date_str[6:8])
    length = len(userlog_items)  # 굳이 사람으로 나눌 필요 없음. 학습 시간의 전체 평균을 구하면 해당 로그 길이로 나눠도 문제 없음.
    my_total, user_total = 0, 0
    my_focus, user_focus = 0, 0
    user_tag_dict = dict()
    user_log_list = []
    for item in userlog_items:
        parsed_t = parse_datetime(str(item.start_time))
        parsed_t2 = parse_datetime(str(item.end_time))
        tt = int((parsed_t2 - parsed_t).total_seconds())
        ft = tt - item.abnormal_time
        if item.user == user:
            my_total += tt // 60
            my_focus += ft // 60
            user_log_list.append(item)
            tag_str = Tag.objects.get(pk=item.tag_id)
            if user_tag_dict.get(tag_str) is None:
                user_tag_dict[tag_str] = tt // 60
            else:
                user_tag_dict[tag_str] += tt // 60
        user_total += tt // 60
        user_focus += ft // 60

    if length != 0:
        user_total //= length

    if length != 0:
        user_focus //= length
    return my_total, user_total, my_focus, user_focus, user_tag_dict, user_log_list


@login_required
def mypage(request):
    context = dict()
    user = request.user

    now_date = str(datetime.datetime.now().strftime('%Y년 %m월'))
    if request.POST:
        now_date = request.POST['new_date']

    my_total, user_total, my_focus, user_focus, user_tag_dict, user_log_list = get_month_data(user, now_date)
    context['now_date'] = now_date
    context['my_total'] = my_total
    context['user_total'] = user_total
    context['my_focus'] = my_focus
    context['user_focus'] = user_focus
    context['user_tag_dict'] = user_tag_dict
    context['user_log_list'] = user_log_list

    return render(request, 'main/mypage.html', context)
