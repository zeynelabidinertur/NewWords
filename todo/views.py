from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render

from tags.models import Tag
from .models import Todo


def show_todo(request):

    if request.method == "POST":
        todo = Todo.objects.create(name=request.POST.get("todo_name"),
                                   description=request.POST.get("description_name"),
                                   owner=request.user)

        todo.tags.add(*request.POST.getlist("tag_names"))

    return render(request, "my_todos.html", {"todos": Todo.objects.filter(owner=request.user.id),
                                             "tags": Tag.objects.all()})


def get_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        if request.user.id != todo.owner.id:
            raise PermissionDenied
        return render(request, "detailed_todo.html", {"todo": todo})
    except Todo.DoesNotExist:
        raise Http404("We don't have any.")
