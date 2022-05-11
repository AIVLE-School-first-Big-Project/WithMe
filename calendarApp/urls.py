from django.urls import path
from .views import todo_new, todo_edit, todo_delete

app_name = 'calendarApp'
urlpatterns = [
    path('todo/new', todo_new, name='todo_new'),
    path('todo/edit/<int:todo_id>', todo_edit, name='todo_edit'),
    path('todo/delete', todo_delete, name='todo_delete'),
]
