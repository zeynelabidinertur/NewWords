from django.conf.urls import url

from .views import show_all_entries, get_entry

urlpatterns = [
    url(r'^$', show_all_entries),
    url(r'^(?P<entry_id>[0-9]+)', get_entry)
]
