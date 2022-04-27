from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect


@login_required
def watch(request):
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        start_time = request.POST.get('a')
        end_time = request.POST.get('b')
        stop_time = request.POST.get('c')


        User_log = User_log(user = User.objects.get(user_id = user_id),
        start_time = start_time,
        pause = stop_time,
        end_time = end_time)

        User_log.save()
        result = '%s %s %s' % (start_time, end_time, stop_time)
        return HttpResponse(result)

    return render(request, 'timer/watch.html')
# Create your views here.



@login_required
def timer(request):

    return render(request, 'timer/timer.html')


@login_required
def stopwatch(request):

    return render(request, 'timer/stopwatch.html')
