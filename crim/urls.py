"""crim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, re_path
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from crim.views.auth import SessionAuth, SessionStatus, SessionClose
from crim.views.main import home, profile
from crim.views.person import PersonList, PersonDetail
from crim.views.user import UserList, UserDetail

admin.autodiscover()

urlpatterns = []

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^admin/', admin.site.urls),
    ]

    urlpatterns += [
        re_path(r'^$', home, name='home'),
        re_path(r'^auth/token/$', obtain_auth_token),
        re_path(r'^auth/session/$', SessionAuth.as_view()),
        re_path(r'^auth/status/$', SessionStatus.as_view()),
        re_path(r'^auth/logout/$', SessionClose.as_view()),
        re_path(r'^profile/', profile),
        re_path(r'^users/$', UserList.as_view(), name='user-list'),
        re_path(r'^user/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),


        re_path(r'^people/$', PersonList.as_view(), name='crimperson-list'),
        re_path(r'^person/(?P<pk>[-a-z0-9]+)/$', PersonDetail.as_view(), name='crimperson-detail'),
    ]

    urlpatterns += [
        re_path(r'^login/$', LoginView.as_view()),
        re_path(r'^logout/$', logout, {'next_page': '/'}),
    ]
