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
from crim.views.genre import GenreList, GenreDetail
from crim.views.mass import MassList, MassDetail
from crim.views.person import PersonList, PersonDetail
from crim.views.piece import PieceList, PieceDetail
from crim.views.observation import ObservationList, ObservationDetail
from crim.views.relationship import RelationshipList, RelationshipDetail
from crim.views.role import RoleList, RoleDetail
from crim.views.roletype import RoleTypeList, RoleTypeDetail
from crim.views.source import SourceList, SourceDetail
from crim.views.treatise import TreatiseList, TreatiseDetail
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
        re_path(r'^user/(?P<username>[0-9]+)/$', UserDetail.as_view(), name='user-detail'),

        re_path(r'^genres/$', GenreList.as_view(), name='crimgenre-list'),
        re_path(r'^genre/(?P<genre_id>[-A-Za-z0-9]+)/$', GenreDetail.as_view(), name='crimgenre-detail'),
        re_path(r'^masses/$', MassList.as_view(), name='crimmass-list'),
        re_path(r'^mass/(?P<mass_id>[-_A-Za-z0-9]+)/$', MassDetail.as_view(), name='crimmass-detail'),
        re_path(r'^observations/$', ObservationList.as_view(), name='crimobservation-list'),
        re_path(r'^observation/(?P<pk>[0-9]+)/$', ObservationDetail.as_view(), name='crimobservation-detail'),
        re_path(r'^people/$', PersonList.as_view(), name='crimperson-list'),
        re_path(r'^person/(?P<person_id>[-_A-Za-z0-9]+)/$', PersonDetail.as_view(), name='crimperson-detail'),
        re_path(r'^pieces/$', PieceList.as_view(), name='crimpiece-list'),
        re_path(r'^piece/(?P<piece_id>[-_A-Za-z0-9]+)/$', PieceDetail.as_view(), name='crimpiece-detail'),
        re_path(r'^relationships/$', RelationshipList.as_view(), name='crimrelationship-list'),
        re_path(r'^relationship/(?P<pk>[0-9]+)/$', RelationshipDetail.as_view(), name='crimrelationship-detail'),
        re_path(r'^roles/$', RoleList.as_view(), name='crimrole-list'),
        re_path(r'^role/(?P<pk>[0-9]+)/$', RoleDetail.as_view(), name='crimrole-detail'),
        re_path(r'^roletypes/$', RoleTypeList.as_view(), name='crimroletype-list'),
        re_path(r'^roletype/(?P<role_type_id>[-A-Za-z0-9]+)/$', RoleTypeDetail.as_view(), name='crimroletype-detail'),
        re_path(r'^sources/$', SourceList.as_view(), name='crimsource-list'),
        re_path(r'^source/(?P<document_id>[-_A-Za-z0-9]+)/$', SourceDetail.as_view(), name='crimsource-detail'),
        re_path(r'^treatises/$', TreatiseList.as_view(), name='crimtreatise-list'),
        re_path(r'^treatise/(?P<document_id>[-_A-Za-z0-9]+)/$', TreatiseDetail.as_view(), name='crimtreatise-detail'),
    ]

    urlpatterns += [
        re_path(r'^login/$', LoginView.as_view()),
        re_path(r'^logout/$', logout, {'next_page': '/'}),
    ]

    urlpatterns += [
        path('pages/', include('django.contrib.flatpages.urls')),
    ]
