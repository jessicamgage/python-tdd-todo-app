"""
This page, unlike superlists/urls.py, is used only for URLs that proceed the lists route; these provide links to URLs for pages that can be accessed specific to links.
"""

from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^(\d+)/share$', views.share_this_list, name='share_this_list'),
    url(r'^users/(.+)/$', views.my_lists, name='my_lists'),
 
]
