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


@login_required
def service(request):
    todo_form = TodoForm()
    todo_list = Todolist.objects.all().filter(Q(author=request.user))
    item = UserLog.objects.filter(Q(user_id=request.user) & Q(end_time__isnull=True))
    if len(item) == 0:
        if request.method == 'POST':
            tag = Tag.objects.get(pk=request.POST['tag_id'])
            user_log = UserLog()
            user_log.user = request.user
            user_log.tag = tag
            user_log.save()

            return render(request, 'timer/service_main.html', {
                "todo_form": todo_form,
                "todo_edit_form": TodoEditForm,
                "todo_list": todo_list,
                "tag": tag,
                "user_log": user_log,
            })
        return render(request, 'main/camera_setting.html')
    else:
        item = item[0]
        tag = Tag.objects.get(pk=item.tag_id)

        return render(request, 'timer/service_main.html', {
            "todo_form": todo_form,
            "todo_edit_form": TodoEditForm,
            "todo_list": todo_list,
            "tag": tag,
            "user_log": item,
        })




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
        time_log.time = timezone.now()
        time_log.event_type = int(data['event_type'])
        time_log.save()

        return JsonResponse(data)