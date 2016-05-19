"""GreedyMusic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, url
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
import os
from app import views
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='view_admin'),
    url(r'^$', views.home, name='view_redirect_home'),
    url(r'^tracks/$', views.list_tracks, name='view_tracklist'),
    url(r'^track/(?P<trackid>[0-9]+)/$', views.get_track, name='view_get_track'),
    url(r'^tracks/add/$', views.add_music_track, name='view_add_track'),
    url(r'^tracks/search/', views.search_music_tracks, name='view_search_track'),
    url(r'^tracks/edit/$', views.edit_track, name='view_edit_track'),
    url(r'^genres/$', views.list_genres, name='view_genrelist'),
    url(r'^genre/(?P<genreid>[0-9]+)/$', views.get_genre, name='view_get_genre'),
    url(r'^genres/add/$', views.add_genre, name='view_add_genre'),
    url(r'^genres/rename/$', views.rename_genre, name='view_rename_genre'),
]

DEBUG = os.environ.get('DEBUG', False)
if not DEBUG:
	urlpatterns.append(url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}))

urlpatterns.append(url(r'^.*$', views.page_not_found, name='view-404-page'))
