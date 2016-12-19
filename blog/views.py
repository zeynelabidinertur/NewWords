# coding=utf-8
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.http import Http404
from .models import MyEntry
from tags.models import Tag


def show_entry(request):

    if request.method == "POST":
        entry = MyEntry.objects.create(header=request.POST.get("header"),
                                       body=request.POST.get("body"),
                                       owner=request.user)

        entry.tags.add(*request.POST.getlist("tag_names"))

    return render(request, "my_blog.html", {"entries": MyEntry.objects.filter(owner=request.user.id),
                                            "tags": Tag.objects.all()})


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
