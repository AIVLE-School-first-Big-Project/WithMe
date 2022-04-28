from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def timer2(request):

    return render(request, 'calendarApp/calendarApp.html')
    # return HttpResponse('hello world')