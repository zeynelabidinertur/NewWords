from django.conf.urls import url

from .views import show_all_entries, get_entry, show_entry

urlpatterns = [
    url(r'^$', show_entry),
    url(r'^(?P<entry_id>[0-9]+)', get_entry)
]
