# coding=utf-8
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .models import myDict


def show_all_entries(request):
    try:
        request.GET.get("blog")
        return render(request, "my_blog.html", {'my_entry': myDict})
    except IndexError:
        raise Http404("We don't have any.")


def get_entry(request, entry_id):
    try:
        i = 0
        for key, val in myDict.items():
            if i == int(entry_id):
                request.GET.get("blog")
                return render(request, "my_blog2.html", {'header': key,
                                                         'body': val})

            i += 1
    except IndexError:
        raise Http404("We don't have that id adress.")
