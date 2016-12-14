# coding=utf-8
from django.shortcuts import render
from django.http import Http404
from .models import MyEntry


def show_all_entries(request):

    try:
        request.GET.get("blog")
        return render(request, "my_blog.html", {"entries": MyEntry.objects.all()})
    except IndexError:
        raise Http404("We don't have any.")


def get_entry(request, entry_id):
    try:
        entry = MyEntry.objects.get(id=entry_id)
        return render(request, "detailed_entry.html", {"entry": entry})
    except IndexError:
        raise Http404("We don't have that id adress.")
