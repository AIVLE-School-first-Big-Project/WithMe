from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect
from timer.forms import *
from tag.models import *
from accounts.models import *
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.utils import timezone
from django.db.models import Q

from calendarApp.form import TodoForm, TodoEditForm
from calendarApp.models import Todolist
from tag.models import Tag
from .models import TimeLog
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import timedelta

def test_result(request):
    context = dict()
    user_log_pk = UserLog.objects.last().id
    item = UserLog.objects.last()
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
            TimeLog(user_log=user_log, time=user_log.start_time,event_type=0).save()
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


@login_required
def watch(request):
    return render(request, 'timer/watch.html')
    
@login_required
def timer(request):
    return render(request, 'timer/timer.html')

@login_required
def stopwatch(request):
    return render(request, 'timer/stopwatch.html')

def get_user_log(current_user):
    try:
        user_log = UserLog.objects.filter(
            user = current_user,
            end_time = None
        ).order_by('start_time')[0]

        #debug
        print('\n'*5)
        print('='*20)
        print(user_log)
        print(user_log.id)
        print(user_log.user.username)
        print('='*20)
        print('\n'*5)

    except UserLog.DoesNotExist:
        user_log = None

    return user_log

def get_tag(tag_name):
    try:
        tag = Tag.objects.get(Tag_name = tag_name)
    except Tag.DoesNotExist:
        tag = None
    return tag

def is_userlog_exist(current_user):
    return get_user_log(current_user) != None

@login_required
def create_userlog(request):
    if request.method == 'POST':
        obj = request.body.decode("utf-8")
        data = json.loads(obj)
        
        if is_userlog_exist(request.user):
            data['result'] = 'false'
            return JsonResponse(data)

        # create user log through ORM
        user_log = UserLog()
        user_log.user = request.user
        user_log.tag = get_tag(data['tag'])
        user_log.save()

        data['result'] = 'true'
        return JsonResponse(data)

@login_required
def create_timelog(request):
    if request.method == 'POST':
        obj = request.body.decode("utf-8")
        data = json.loads(obj)

        # create user log through ORM
        time_log = TimeLog()
        time_log.user_log = get_user_log(request.user)
        time_log.event_type = int(data['event_type'])
        time_log.save()

        return JsonResponse(data)