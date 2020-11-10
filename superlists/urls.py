//This file wires up site-wide URLs with the usage of regular expressions, URLs for separate routes using list and account URLs, and the views pulled from views.py

from django.conf.urls import include, url
from lists import views as list_views
from lists import urls as list_urls
from accounts import urls as accounts_urls

urlpatterns = [
    url(r'^$', list_views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),
    url(r'^accounts/', include(accounts_urls)),
]
