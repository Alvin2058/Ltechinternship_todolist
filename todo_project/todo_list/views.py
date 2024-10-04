from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Todo
from django.utils.dateparse import parse_date
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage


# creating a new to do list
@method_decorator(csrf_exempt, name='dispatch')
class TodoCreate(View):
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            due_date=parse_date(data.get('due_date'))
            if due_date is None:
                return JsonResponse({'error':'please enter a date'})
            if due_date < timezone.now().date():
                # print(timezone.now().date)
                return JsonResponse({'error':'Please enter a valid year'},status=400)

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
        
        # Gettng the page number and number of tasks ina single page
        page_num = request.GET.get('page_num', 1)
        items_in_page = request.GET.get('items_in_page', 5)  
        # default number of tasks is 5

        # Converting the strings to integers
        try:
            page_num = int(page_num)
            items_in_page = int(items_in_page)
        except ValueError:
            return JsonResponse({'error': 'Invalid page number or items per page'}, status=400)

        paginator = Paginator(todos, items_in_page)

        try:
            todo_page = paginator.page(page_num)
        except EmptyPage:
            return JsonResponse({'error': 'No more items'}, status=404)

        # response the user will see 
        response_data = {
            'todos': list(todo_page),
            'total_pages': paginator.num_pages,
            'current_page': todo_page.number,
        }

        return JsonResponse(response_data, safe=False, status=200)
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
            data = json.loads(request.body)
            todo = Todo.objects.get(id=todo_id)

            due_date=parse_date(data.get('due_date'))
            if due_date < timezone.now().date():
                return JsonResponse({'error':'Please enter a valid year'},status=400)
 
            todo.title = data.get('title', todo.title)
            todo.description = data.get('description', todo.description)
            todo.due_date = parse_date(data.get('due_date', str(todo.due_date)))
            todo.status = data.get('status', todo.status)
            
            todo.save()
            return JsonResponse({'message': 'Todo updated successfully'}, status=200)
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class TodoDelete(View):
    def delete(self, request, todo_id):
        try:
            todo = Todo.objects.get(id=todo_id)
            todo.delete()
            return JsonResponse({'message': 'Todo deleted successfully'}, status=204)
        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)
