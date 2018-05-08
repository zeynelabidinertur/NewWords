from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', show_all_books),
    url(r'^(?P<book_id>[0-9]+)', get_book),
    url(r'^add/$', add_book),
]
