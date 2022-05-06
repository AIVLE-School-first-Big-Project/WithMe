from django.urls import path
from .views import *

app_name = 'calendarApp'
urlpatterns = [
    path('', timer2, name='timer2'),
    path('todo/new', todo_new,  name='todo_new'),
    path('todo/edit/<int:todo_id>', todo_edit,  name='todo_edit'),
    path('todo/delete', todo_delete, name='todo_delete'),
]