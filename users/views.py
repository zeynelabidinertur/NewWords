from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.models import User
# Create your views here.


def show_profile(request):
    return HttpResponseRedirect("/blog")


def signup(request):

    if request.method == "POST":
        User.objects.create_user(username=request.POST.get("username"),
                            password=request.POST.get("password"))
        return HttpResponse("Success!")

    return render(request, "register.html")
