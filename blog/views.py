# coding=utf-8
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import Http404
from .models import MyEntry
from tags.models import Tag
from .forms import BlogForm
from .models import MyEntry


def show_entry(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = request.user
            entry.save()
            form.save_m2m()

    elif request.method == "GET":
        form = BlogForm()

    return render(request, "my_blog.html", {"entries": MyEntry.objects.filter(owner=request.user.id),
                                            "tags": Tag.objects.all(),
                                            "form": form})


def show_all_entries(request):

    try:
        request.GET.get("blog")
        return render(request, "my_blog.html", {"entries": MyEntry.objects.all()})
    except IndexError:
        raise Http404("We don't have any.")


def get_entry(request, entry_id):
    try:
        entry = MyEntry.objects.get(id=entry_id)
        if request.user.id != entry.owner.id:
            raise PermissionDenied
        return render(request, "detailed_entry.html", {"entry": entry})
    except IndexError:
        raise Http404("We don't have that id adress.")


@permission_required('is_superuser')
def show_all_entries(request):
    return render(request, "my_blog.html", {"entries": MyEntry.objects.all()})


@permission_required('is_superuser')
def show_all_entries_from_user(request, user_id):
    return render(request, "my_blog.html", {"entries": MyEntry.objects.filter(owner=user_id)})
