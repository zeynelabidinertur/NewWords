from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', show_entry),
    url(r'^(?P<entry_id>[0-9]+)', get_entry),
    url(r'^entries/all/$', show_all_entries),
    url(r'^entries/all/user/(?P<user_id>[0-9]+)$', show_all_entries_from_user),
]
