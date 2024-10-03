from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Todo
from django.utils.dateparse import parse_date
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# creating a new to do list
@method_decorator(csrf_exempt, name='dispatch')
class TodoCreate(View):
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            todo = Todo.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                due_date=parse_date(data.get('due_date')),
                status=data.get('status', 'pending')
            )
            return JsonResponse({'id': todo.id, 'message': 'Todo created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# viewing a list of tasks
class TodoList(View):
    def get(self, request):
        todos = Todo.objects.all().values()
        return JsonResponse(list(todos), safe=False, status=200)


# viewing a specific list of tasks
class TodoDetail(View):
    def get(self, request, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id)
            return JsonResponse({
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'due_date': todo.due_date,
                'status': todo.status
            }, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)
        
# updating the to_do tasks
@method_decorator(csrf_exempt, name='dispatch')
class TodoUpdate(View):
    def put(self, request, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id)
            data = json.loads(request.body)
            
            todo.title = data.get('title', todo.title)
            todo.description = data.get('description', todo.description)
            todo.due_date = parse_date(data.get('due_date', str(todo.due_date)))
            todo.status = data.get('status', todo.status)
            
            todo.save()
            return JsonResponse({'message': 'Todo updated successfully'}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)

class TodoDelete(View):
    def delete(self, request, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            return JsonResponse({'message': 'Todo deleted successfully'}, status=204)
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)
