from django.conf.urls import url

from .views import show_todo, get_todo

urlpatterns = [
    url(r'^$', show_todo),
    url(r'^(?P<todo_id>[0-9]+)', get_todo)
]
