from django.urls import path
from .views import TodoCreate, TodoList, TodoDetail, TodoUpdate, TodoDelete

urlpatterns = [
    path('todos', TodoList.as_view(), name='todo-list'),
    path('todos/create', TodoCreate.as_view(), name='todo-create'),
    path('todos/<int:todo_id>', TodoDetail.as_view(), name='todo-detail'),
    path('todos/<int:todo_id>/update', TodoUpdate.as_view(), name='todo-update'),
    path('todos/<int:todo_id>/delete', TodoDelete.as_view(), name='todo-delete'),
]
