from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render

from tags.models import Tag
from users.models import *
from .forms import *
from .models import Book


def show_all_books(request):
    try:
        request.GET.get("book")
        # return render(request, "my_books.html", {"books": Book.objects.all()})
    except IndexError:
        raise Http404("We don't have any.")
    return render(request, "my_books.html", {"books": Book.objects.filter(owner=request.user.id)})


def get_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        return render(request, "my_books.html", {"book": book})
    except Book.DoesNotExist:
        raise Http404("We don't have any.")


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            form.save_m2m()

    elif request.method == "GET":
        form = BookForm()

    return render(request, "my_books.html", {"books": Book.objects.filter(owner=request.user.id),
                                             "tags": Tag.objects.all(),
                                             "form": form})

@permission_required('is_superuser')
def show_all_todo_from_user(request, user_id):
    return render(request, "my_todos.html", {"books": Book.objects.filter(owner=user_id)})
