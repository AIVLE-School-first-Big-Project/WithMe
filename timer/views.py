from django.shortcuts import render
from django.http import HttpResponse



def watch(request):
    if request.method == 'POST':
        start_time = request.POST.get('a')
        end_time = request.POST.get('b')
        stop_time = request.POST.get('c')
        result = '%s %s %s' % (start_time, end_time, stop_time)
        return HttpResponse(result)
    return render(request, 'timer/watch.html')
# Create your views here.
