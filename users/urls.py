from django.conf.urls import url, include

from .views import signup

urlpatterns = [
    url(r'^sign_in/$', signup),
    url(r'', include("django.contrib.auth.urls"))

]
