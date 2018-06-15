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
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token

from crim.views.auth import SessionAuth, SessionStatus, SessionClose
from crim.views.main import home, profile
from crim.views.genre import GenreList
from crim.views.mass import MassList, MassDetail
from crim.views.person import PersonList, PersonDetail
from crim.views.observation import ObservationList, ObservationDetail
from crim.views.relationship import RelationshipList, RelationshipDetail
from crim.views.piece import PieceList, ModelList, PieceDetail, PieceWithObservations, PieceWithRelationships
from crim.views.roletype import RoleTypeList
from crim.views.search import FacetedSearchForm, FacetedSearchView
from crim.views.source import SourceList, SourceDetail
from crim.views.treatise import TreatiseList, TreatiseDetail
from crim.views.user import UserList, UserDetail

# The following are for the JSON views
from crim.views.genre import GenreListData, GenreDetailData
from crim.views.mass import MassListData, MassDetailData
from crim.views.part import PartListData, PartDetailData
from crim.views.person import PersonListData, PersonDetailData
from crim.views.phrase import PhraseListData, PhraseDetailData
from crim.views.piece import PieceListData, ModelListData, PieceDetailData, PieceWithObservationsData, PieceWithRelationshipsData
from crim.views.observation import ObservationListData, ObservationDetailData
from crim.views.relationship import RelationshipListData, RelationshipDetailData
from crim.views.role import RoleListData, RoleDetailData
from crim.views.roletype import RoleTypeListData, RoleTypeDetailData
from crim.views.source import SourceListData, SourceDetailData
from crim.views.treatise import TreatiseListData, TreatiseDetailData
from crim.views.voice import VoiceListData, VoiceDetailData

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

        re_path(r'^search/', FacetedSearchView(form_class=FacetedSearchForm), name='search'),

        re_path(r'^genres/$', GenreList.as_view(), name='crimgenre-list'),
        re_path(r'^genre/(?P<genre_id>[-A-Za-z0-9]+)/$', RedirectView.as_view(url='/pieces/?genre=%(genre_id)s', permanent=False), name='crimgenre-detail'),
        re_path(r'^masses/$', MassList.as_view(), name='crimmass-list'),
        re_path(r'^mass/(?P<mass_id>[-_A-Za-z0-9]+)/$', MassDetail.as_view(), name='crimmass-detail'),
        re_path(r'^mass/(?P<mass_id>[-_A-Za-z0-9]+)/(?P<movement_number>[0-9]+)/$', RedirectView.as_view(url='/piece/%(mass_id)s_%(movement_number)s/', permanent=True), name='crimmassmovement-detail'),
        re_path(r'^models/$', ModelList.as_view(), name='crimmodel-list'),
        re_path(r'^observations/$', ObservationList.as_view(), name='crimobservation-list'),
        re_path(r'^observation/(?P<pk>[0-9]+)/$', ObservationDetail.as_view(), name='crimobservation-detail'),
        re_path(r'^people/$', PersonList.as_view(), name='crimperson-list'),
        re_path(r'^person/(?P<person_id>[-_A-Za-z0-9]+)/$', PersonDetail.as_view(), name='crimperson-detail'),
        re_path(r'^pieces/$', PieceList.as_view(), name='crimpiece-list'),
        re_path(r'^piece/(?P<piece_id>[-_A-Za-z0-9]+)/$', PieceDetail.as_view(), name='crimpiece-detail'),
        re_path(r'^piece/(?P<piece_id>[-_A-Za-z0-9]+)/observations/$', PieceWithObservations.as_view(), name='crimpiece-observations-detail'),
        re_path(r'^piece/(?P<piece_id>[-_A-Za-z0-9]+)/relationships/$', PieceWithRelationships.as_view(), name='crimpiece-relationships-detail'),
        re_path(r'^relationships/$', RelationshipList.as_view(), name='crimrelationship-list'),
        re_path(r'^relationship/(?P<pk>[0-9]+)/$', RelationshipDetail.as_view(), name='crimrelationship-detail'),
        re_path(r'^roletypes/$', RoleTypeList.as_view(), name='crimroletype-list'),
        re_path(r'^roletype/(?P<role_type_id>[-A-Za-z0-9]+)/$', RedirectView.as_view(url='/people/?role=%(role_type_id)s', permanent=False), name='crimroletype-detail'),
        re_path(r'^sources/$', SourceList.as_view(), name='crimsource-list'),
        re_path(r'^source/(?P<document_id>[-_A-Za-z0-9]+)/$', SourceDetail.as_view(), name='crimsource-detail'),
        re_path(r'^treatises/$', TreatiseList.as_view(), name='crimtreatise-list'),
        re_path(r'^treatise/(?P<document_id>[-_A-Za-z0-9]+)/$', TreatiseDetail.as_view(), name='crimtreatise-detail'),
        # The following are for the JSON views
        re_path(r'^data/genres/$', GenreListData.as_view(), name='crimgenre-list-data'),
        re_path(r'^data/genre/(?P<genre_id>[-A-Za-z0-9]+)/$', GenreDetailData.as_view(), name='crimgenre-detail-data'),
        re_path(r'^data/masses/$', MassListData.as_view(), name='crimmass-list-data'),
        re_path(r'^data/mass/(?P<mass_id>[-_A-Za-z0-9]+)/$', MassDetailData.as_view(), name='crimmass-detail-data'),
        re_path(r'^data/mass/(?P<mass_id>[-_A-Za-z0-9]+)/(?P<movement_number>[0-9]+)/$', RedirectView.as_view(url='/data/piece/%(mass_id)s_%(movement_number)s/', permanent=True), name='crimmassmovement-detail-data'),
        re_path(r'^data/models/$', ModelListData.as_view(), name='crimmodel-list-data'),
        re_path(r'^data/observations/$', ObservationListData.as_view(), name='crimobservation-list-data'),
        re_path(r'^data/observation/(?P<pk>[0-9]+)/$', ObservationDetailData.as_view(), name='crimobservation-detail-data'),
        re_path(r'^data/parts/$', PartListData.as_view(), name='crimpart-list-data'),
        re_path(r'^data/part/(?P<part_id>[-_A-Za-z0-9\.]+)/$', PartDetailData.as_view(), name='crimpart-detail-data'),
        re_path(r'^data/people/$', PersonListData.as_view(), name='crimperson-list-data'),
        re_path(r'^data/person/(?P<person_id>[-_A-Za-z0-9]+)/$', PersonDetailData.as_view(), name='crimperson-detail-data'),
        re_path(r'^data/phrases/$', PhraseListData.as_view(), name='crimphrase-list-data'),
        re_path(r'^data/phrase/(?P<phrase_id>[-_A-Za-z0-9:]+)/$', PhraseDetailData.as_view(), name='crimphrase-detail-data'),
        re_path(r'^data/pieces/$', PieceListData.as_view(), name='crimpiece-list-data'),
        re_path(r'^data/piece/(?P<piece_id>[-_A-Za-z0-9]+)/$', PieceDetailData.as_view(), name='crimpiece-detail-data'),
        re_path(r'^data/piece/(?P<piece_id>[-_A-Za-z0-9]+)/observations/$', PieceWithObservationsData.as_view(), name='crimpiece-observations-detail-data'),
        re_path(r'^data/piece/(?P<piece_id>[-_A-Za-z0-9]+)/relationships/$', PieceWithRelationshipsData.as_view(), name='crimpiece-relationships-detail-data'),
        re_path(r'^data/relationships/$', RelationshipListData.as_view(), name='crimrelationship-list-data'),
        re_path(r'^data/relationship/(?P<pk>[0-9]+)/$', RelationshipDetailData.as_view(), name='crimrelationship-detail-data'),
        re_path(r'^data/roles/$', RoleListData.as_view(), name='crimrole-list-data'),
        re_path(r'^data/role/(?P<pk>[0-9]+)/$', RoleDetailData.as_view(), name='crimrole-detail-data'),
        re_path(r'^data/roletypes/$', RoleTypeListData.as_view(), name='crimroletype-list-data'),
        re_path(r'^data/roletype/(?P<role_type_id>[-A-Za-z0-9]+)/$', RoleTypeDetailData.as_view(), name='crimroletype-detail-data'),
        re_path(r'^data/sources/$', SourceListData.as_view(), name='crimsource-list-data'),
        re_path(r'^data/source/(?P<document_id>[-_A-Za-z0-9]+)/$', SourceDetailData.as_view(), name='crimsource-detail-data'),
        re_path(r'^data/treatises/$', TreatiseListData.as_view(), name='crimtreatise-list-data'),
        re_path(r'^data/treatise/(?P<document_id>[-_A-Za-z0-9]+)/$', TreatiseDetailData.as_view(), name='crimtreatise-detail-data'),
        re_path(r'^data/voices/$', VoiceListData.as_view(), name='crimvoice-list-data'),
        re_path(r'^data/voice/(?P<voice_id>[-_A-Za-z0-9\(\)]+)/$', VoiceDetailData.as_view(), name='crimvoice-detail-data'),
    ]

    urlpatterns += [
        re_path(r'^login/$', LoginView.as_view()),
        re_path(r'^logout/$', logout, {'next_page': '/'}),
    ]

    urlpatterns += [
        path('pages/', include('django.contrib.flatpages.urls')),
    ]
