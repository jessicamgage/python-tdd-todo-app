"""
These URLs are specific to the accounts route -- any URL that is accessed via the accounts route, such as sending a login email, is used with these URLs.
So, unlike the urls.py file in superlists, these are not site-wide URLs.
"""
from django.conf.urls import url
from django.contrib.auth.views import logout
from accounts import views

urlpatterns = [
   url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
   url(r'^login$', views.login, name='login'),
   url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]
