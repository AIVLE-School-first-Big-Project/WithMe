from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect
from timer.forms import *
from tag.models import *
from django.http import HttpResponseRedirect, JsonResponse
import json
from django.utils import timezone

@login_required
def watch(request):
    form = timeForm(request.POST)
    if request.method == 'POST':
        if form.is_valid(): # 데이터 저장/ 어딘가로 이동/메세지 출력 등등
            timer_data = form.save(commit = False)
            timer_data.tag_name = request.POST.get('Tag')
            timer_data.start_time = request.POST.get('a') 
            timer_data.end_time = request.POST.get('b')
            timer_data.pause = request.POST.get('c')
            timer_data.save()
            return redirect('timer:watch')
        else:
            form = timeForm()
    return render(request, 'timer/watch.html', {'form':form})
    
@login_required
def timer(request):

    return render(request, 'timer/timer.html')


@login_required
def stopwatch(request):

    return render(request, 'timer/stopwatch.html')

@login_required
def set_start_time(request):
    obj = request.body.decode("utf-8")
    data = json.loads(obj)

    start_time = data['time']
    tag = data['tag']
    print('\n'*5, f'{type(start_time)}|| start_time : {start_time}', '\n'*5)
    print('\n'*5, f'{type(tag)}|| tag : {tag}', '\n'*5)

    # user_log = UserLog()
    # user_log.user = request.user
    # user_log.tag = Tag.objects.get(id=tag_id)
    # user_log.start_time = timezone.now()
    # user_log.save()

    return JsonResponse(data)