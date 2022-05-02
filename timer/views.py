from audioop import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import redirect


@login_required
def watch(request):
    
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        tag_name = request.POST.get(tag_name)
        start_time = request.POST.get(start_time)
        end_time = request.POST.get(end_time)
        stop_time = request.POST.get(stop_time)


        New_User_log = User_log()
        New_User_log.start_time = start_time
        New_User_log.pause = stop_time
        New_User_log.end_time = end_time

        User_log.save()
        
        return HttpResponseRedirect(reverse('timer/watch.html'))

    return render(request, 'timer/watch.html')
# Create your views here.



@login_required
def timer(request):

    return render(request, 'timer/timer.html')


@login_required
def stopwatch(request):

    return render(request, 'timer/stopwatch.html')
