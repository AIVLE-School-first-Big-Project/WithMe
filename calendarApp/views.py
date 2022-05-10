from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .form import TodoForm, TodoEditForm
from .models import Todolist
import json
# Create your views here.
@login_required
def timer2(request):

    return render(request, 'calendarApp/calendarApp.html')
    # return HttpResponse('hello world')



@login_required
def todo_new(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return render(request, "timer/todo_item.html", {
                    "todo": todo,
                })

            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        form = TodoForm()
        return render(request, 'calendarApp/todo_new.html', {
            "form": form
        })



@login_required
def todo_edit(request, todo_id):
    item = Todolist.objects.get(id=todo_id)
    if request.method == 'POST':
        form = TodoEditForm(request.POST, instance=item)
        if form.is_valid():
            todo = form.save()
            if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return render(request, "timer/todo_item.html", {
                    "todo": todo,
                })
    else:
        form = TodoEditForm(instance=item)
        return render(request, 'calendarApp/todo_edit.html', {
            "form": form,
            "todo_id": todo_id,
        })

@login_required
def todo_delete(request):
    if request.method == 'POST':
        item = Todolist.objects.get(id=request.POST['todo_id'])
        item.delete()
        item = Todolist.objects.all()

        return HttpResponse(json.dumps({'cnt':len(item)}), content_type = "application/json")