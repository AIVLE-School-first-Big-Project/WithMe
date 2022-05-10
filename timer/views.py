from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from calendarApp.form import TodoForm, TodoEditForm
from calendarApp.models import Todolist
from tag.models import Tag
from .models import TimeLog, UserLog


def test_result(request):
    if request.POST:
        context = dict()
        user_log_pk = request.POST['user_log']
        item = UserLog.objects.get(id=user_log_pk)
        context['user_log'] = item

        total_time, total_focus_time = 0, 0
        for i in UserLog.objects.all().filter(Q(tag=item.tag)):
            parsed_t = parse_datetime(str(i.start_time))
            parsed_t2 = parse_datetime(str(i.end_time))
            tt = int((parsed_t2 - parsed_t).total_seconds())
            total_time += tt
            total_focus_time += tt - i.abnormal_time
        context['total_time'] = total_time
        context['total_focus_time'] = total_focus_time
        pattern_list = []

        lst = TimeLog.objects.all().filter(Q(user_log=user_log_pk)).order_by('time')
        for idx, i in enumerate(lst):
            e = 1 if i.event_type == 0 else 0

            if e == 0:
                res = dict()
                later = i.time - timedelta(seconds=1)
                res['x'] = later.strftime("%Y-%m-%d %H:%M:%S")
                res['y'] = 1
                pattern_list.append(res)

            if e == 1:
                if idx != 0:
                    res = dict()
                    later = i.time - timedelta(seconds=1)
                    res['x'] = later.strftime("%Y-%m-%d %H:%M:%S")
                    res['y'] = 0
                    pattern_list.append(res)
            res = dict()
            res['x'] = i.time.strftime("%Y-%m-%d %H:%M:%S")
            res['y'] = e
            pattern_list.append(res)

        res = dict()
        res['x'] = item.end_time.strftime("%Y-%m-%d %H:%M:%S")
        res['y'] = 1
        pattern_list.append(res)
        context['pattern_list'] = pattern_list
        return render(request, 'timer/service_result2.html', context)
    else:
        return redirect('mypage')


@login_required
def service(request):
    context = dict()
    context['todo_form'] = TodoForm
    context['todo_edit_form'] = TodoEditForm
    context['todo_list'] = Todolist.objects.all().filter(Q(author=request.user))

    item = UserLog.objects.filter(Q(user_id=request.user) & Q(end_time__isnull=True))
    if len(item) == 0:
        if request.method == 'POST':
            context['tag'] = Tag.objects.get(pk=request.POST['tag_id'])
            user_log = UserLog()
            user_log.user = request.user
            user_log.tag = context['tag']
            user_log.save()
            TimeLog(user_log=user_log, time=user_log.start_time, event_type=0).save()
            context['user_log'] = user_log
            return render(request, 'timer/service_main.html', context)
        return render(request, 'main/camera_setting.html')
    else:
        user_log = item[0]
        context['tag'] = Tag.objects.get(pk=user_log.tag_id)
        context['user_log'] = user_log
        return render(request, 'timer/service_main.html', context)


@login_required
def result(request):
    if request.method == 'POST':
        context = dict()
        user_log_pk = request.POST['user_log']
        item = UserLog.objects.get(id=user_log_pk)
        item.end_time = timezone.now()
        item.save()
        context['user_log'] = item

        total_time, total_focus_time = 0, 0
        for i in UserLog.objects.all().filter(Q(tag=item.tag)):
            parsed_t = parse_datetime(str(i.start_time))
            parsed_t2 = parse_datetime(str(i.end_time))
            tt = int((parsed_t2 - parsed_t).total_seconds())
            total_time += tt
            total_focus_time += tt - i.abnormal_time
        context['total_time'] = total_time
        context['total_focus_time'] = total_focus_time
        pattern_list = []

        lst = TimeLog.objects.all().filter(Q(user_log=user_log_pk)).order_by('time')
        for idx, i in enumerate(lst):
            e = 1 if i.event_type == 0 else 0

            if e == 0:
                res = dict()
                later = i.time - timedelta(seconds=1)
                print(idx, '>>', later)
                res['x'] = later.strftime("%Y-%m-%d %H:%M:%S")
                res['y'] = 1
                pattern_list.append(res)

            if e == 1:
                if idx != 0:
                    res = dict()
                    later = i.time - timedelta(seconds=1)
                    res['x'] = later.strftime("%Y-%m-%d %H:%M:%S")
                    res['y'] = 0
                    pattern_list.append(res)
            res = dict()
            res['x'] = i.time.strftime("%Y-%m-%d %H:%M:%S")
            res['y'] = e
            pattern_list.append(res)

        res = dict()
        res['x'] = item.end_time.strftime("%Y-%m-%d %H:%M:%S")
        res['y'] = 1
        pattern_list.append(res)
        context['pattern_list'] = pattern_list
        return render(request, 'timer/service_result.html', context)
    else:
        return redirect('service')
