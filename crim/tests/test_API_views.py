"""
This is the test_API_views.py file for CRIM project.

This file is part of the Django Testing part of the crim application.
The testing component consists of several parts testing all the models,
views, API views, and their respective methods in order to ensure the
proper functionality of the applicaiton. Whenever an engineer implements
any major changes to the CRIM project, they should run the test suite locally
to ensure that the application architecture is maintained and all core methods
return desired results.

This specific module tests CRIM API Views. API Views are Python methods that
configure the displayed content based on the requests to and returns of the
Django REST API that is part of the CRIM application. This file tests their
constructors and class methods.

@author: Oleh Shostak '24
@version: 1.0
@created: 7/3/22

To-do's:

-> CRIMDefinition (id parameter doesn't work)
-> Relationship (figure out list serializer)

"""

from crim.models.person import CRIMPerson
from crim.models.genre import CRIMGenre
from crim.models.role import CRIMRoleType
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.person import CRIMPersonListSerializer, CRIMPersonDetailSerializer
from crim.models.person import CRIMPerson
from crim.models.definition import CRIMDefinition
from crim.models.document import CRIMDocument, CRIMTreatise, CRIMSource
from crim.models.role import CRIMRole, CRIMRoleType
from crim.models.forum import CRIMForumPost
from crim.models.genre import CRIMGenre
from crim.models.piece import CRIMPiece
from crim.models.voice import CRIMVoice
from crim.models.mass import CRIMMass
from crim.models.note import CRIMNote
from crim.models.user import CRIMUserProfile
from crim.models.observation import CJObservation
from crim.models.part import CRIMPart
from crim.models.phrase import CRIMPhrase
from crim.models.piece import CRIMPiece, CRIMModel, CRIMMassMovement
from crim.models.relationship import CJRelationship

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.urls import reverse
from mixer.backend.django import mixer
from model_bakery import baker
from playwright.sync_api import sync_playwright

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate


import re

# Genre
class GenreDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyPiece = baker.make(CRIMPiece, genre=self.dummyGenre)

    def test_data_genre_list_view(self):
        url = reverse('crimgenre-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyGenre.genre_id, response.data[0]["genre_id"])

    def test_data_genre_detail_view(self):
        url = reverse("crimgenre-detail-data", kwargs={"genre_id": "testDataGenre"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyGenre.genre_id, response.data["genre_id"])

# Mass
class MassDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyMass = baker.make(CRIMMass, genre=self.dummyGenre, mass_id="testMass")

    def test_data_mass_list_view(self):
        url = reverse('crimmass-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyMass.mass_id, response.data[0]["mass_id"])

    def test_data_mass_detail_view(self):
        url = reverse("crimmass-detail-data", kwargs={"mass_id": "testMass"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyMass.mass_id, response.data["mass_id"])

# Model
class ModelDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyMassMovement = baker.make(CRIMMassMovement, genre=self.dummyGenre, title="testModel")

    def test_data_model_list_view(self):
        url = reverse('crimmodel-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyMassMovement.title, response.data[0]["title"])

# Observation
class ObservationDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyObservation = baker.make(CJObservation, id=1, curated=True, observer=baker.make(CRIMPerson, person_id="testObservationPerson"), piece=baker.make(CRIMPiece), definition=baker.make(CRIMDefinition))

    def test_data_observation_list_view(self):
        url = reverse('cjobservation-list-data')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyObservation.id, response.data[0]["id"])

    def test_data_observation_list_brief_view(self):
        url = reverse('cjobservation-list-brief-data')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyObservation.id, response.data[0]["id"])

    def test_data_observation_detail_view(self):
        url = reverse("cjobservation-detail-data", kwargs={"id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyObservation.id, response.data["id"])

    def test_data_new_observation_view(self):
        url = reverse('cjobservation-new-data')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Parts
class PartDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyPart = baker.make(CRIMPart, part_id=1, name="testPart", piece=baker.make(CRIMPiece))

    def test_data_part_list_view(self):
        url = reverse('crimpart-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPart.name, response.data[0]["name"])

    def test_data_part_detail_view(self):
        url = reverse("crimpart-detail-data", kwargs={"part_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPart.name, response.data["name"])

# Person
class PersonDataViewTest(APITestCase):
    def setUp(self):
        self.dummyPerson = baker.make(CRIMPerson, person_id=1, name="testPerson")

    def test_data_person_list_view(self):
        url = reverse('crimperson-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPerson.name, response.data[0]["name"])

    def test_data_person_detail_view(self):
        url = reverse("crimperson-detail-data", kwargs={"person_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPerson.name, response.data["name"])

# Phrase
class PhraseDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyPhrase = baker.make(CRIMPhrase, phrase_id=1, piece=baker.make(CRIMPiece), part=baker.make(CRIMPart, name="testPart"))

    def test_data_phrase_list_view(self):
        url = reverse('crimphrase-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPhrase.part.name, response.data[0]["part"]["name"])

    def test_data_phrase_detail_view(self):
        url = reverse("crimphrase-detail-data", kwargs={"phrase_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPhrase.part.name, response.data["part"]["name"])

# Piece
class PieceDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyPiece = baker.make(CRIMMassMovement, title="testPiece", piece_id=1, remarks="YO", genre=self.dummyGenre, composer=baker.make(CRIMPerson, name="testPiecePerson"))

    def test_data_piece_list_view(self):
        url = reverse('crimpiece-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPiece.title, response.data[0]["title"])

    def test_data_piece_detail_view(self):
        url = reverse("crimpiece-detail-data", kwargs={"piece_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPiece.title, response.data["title"])

    def test_data_piece_relationships_detail_view(self):
        url = reverse("crimpiece-relationships-detail-data", kwargs={"piece_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyPiece.title, response.data["title"])

# Relationship
class RelationshipDataViewTest(APITestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testDataGenre", genre_id="testDataGenre")
        self.dummyRelationship = baker.make(CJRelationship, id=1, curated=True, observer=baker.make(CRIMPerson, person_id="testRelationshipPerson"), definition=baker.make(CRIMDefinition), derivative_observation=baker.make(CJObservation), model_observation=baker.make(CJObservation), model_piece=baker.make(CRIMPiece), derivative_piece=baker.make(CRIMPiece))

    def test_data_relationship_list_view(self):
        url = reverse('cjrelationship-list-data')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.dummyRelationship.id, response.data[0]["id"])

    def test_data_relationship_list_brief_view(self):
        url = reverse('cjrelationship-list-brief-data')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.dummyObservation.id, response.data[0]["id"])

    def test_data_relationship_detail_view(self):
        url = reverse("cjrelationship-detail-data", kwargs={"id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyRelationship.id, response.data["id"])

    def test_data_new_relationship_view(self):
        url = reverse('cjrelationship-new-data')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Role
class RoleDataViewTest(APITestCase):
    def setUp(self):
        self.dummyRoleType = baker.make(CRIMRoleType, id=1, role_type_id=1, name="testRoleType")
        self.dummyRole = baker.make(CRIMRole, role_type=self.dummyRoleType, person=baker.make(CRIMPerson, person_id="testRolePerson"))

    def test_data_role_list_view(self):
        url = reverse('crimrole-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyRole.person.person_id, response.data[0]["person"])

    def test_data_role_detail_view(self):
        url = reverse("crimrole-detail-data", kwargs={"id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyRole.person.person_id, response.data["person"])

# RoleType
class RoleTypeDataViewTest(APITestCase):
    def setUp(self):
        self.dummyRoleType = baker.make(CRIMRoleType, id=1, role_type_id=1, name="testRoleType")

    def test_data_roletype_list_view(self):
        url = reverse('crimroletype-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(self.dummyRoleType.name, response.data[0]["name"])

    def test_data_roletype_detail_view(self):
        self.dummyRoleTypeDetail = baker.make(CRIMRoleType, id=1, role_type_id="analyst", name="testRoleType")
        self.dummyRole = baker.make(CRIMRole, role_type=self.dummyRoleTypeDetail, person=baker.make(CRIMPerson, person_id="testRolePerson"))
        url = reverse("crimroletype-detail-data", kwargs={"role_type_id": "analyst"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyRoleType.name, response.data["name"])

# Source
class SourceDataViewTest(APITestCase):
    def setUp(self):
        self.dummySource = baker.make(CRIMSource, document_id=1, title="testSource")

    def test_data_source_list_view(self):
        url = reverse('crimsource-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummySource.title, response.data[0]["title"])

    def test_data_source_detail_view(self):
        url = reverse("crimsource-detail-data", kwargs={"document_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummySource.title, response.data["title"])

# Treatise
class TreatiseDataViewTest(APITestCase):
    def setUp(self):
        self.dummyTreatise = baker.make(CRIMTreatise, document_id=1, title="testTreatise")

    def test_data_treatise_list_view(self):
        url = reverse('crimtreatise-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyTreatise.title, response.data[0]["title"])

    def test_data_treatise_detail_view(self):
        url = reverse("crimtreatise-detail-data", kwargs={"document_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyTreatise.title, response.data["title"])

# Voice
class VoiceDataViewTest(APITestCase):
    def setUp(self):
        self.dummyVoice = baker.make(CRIMVoice, voice_id=1, original_name="testVoice", piece=baker.make(CRIMPiece))

    def test_data_voice_list_view(self):
        url = reverse('crimvoice-list-data')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyVoice.original_name, response.data[0]["original_name"])

    def test_data_voice_detail_view(self):
        url = reverse("crimvoice-detail-data", kwargs={"voice_id": 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dummyVoice.original_name, response.data["original_name"])
