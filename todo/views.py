# Create your views here.
from django.http import Http404
from django.shortcuts import render
from .models import Todo


def show_todo(request):

    if request.method == "POST":
        Todo.objects.create(name=request.POST.get("todo_name"),
                            description=request.POST.get("description_name"))

    return render(request, "my_todos.html", {"todos": Todo.objects.all()})


def get_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        return render(request, "detailed_todo.html", {"todo": todo})
    except Todo.DoesNotExist:
        raise Http404("We don't have any.")
