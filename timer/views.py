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

@login_required
def watch(request):
    return render(request, 'timer/watch.html')
    
@login_required
def timer(request):
    return render(request, 'timer/timer.html')

@login_required
def stopwatch(request):
    return render(request, 'timer/stopwatch.html')

def get_user_log(user):
    user_log = None # UserLog()
    return user_log

def get_tag(tag_name):
    tag = None # UserLog()
    return tag

@login_required
def create_userlog(request):
    if request.method == 'POST':
        obj = request.body.decode("utf-8")
        data = json.loads(obj)
        
        # create user log through ORM
        user_log = UserLog()
        user_log.user = request.user
        user_log.tag = get_tag(data['tag'])
        user_log.save()

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