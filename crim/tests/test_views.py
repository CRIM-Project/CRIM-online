"""
This is the test_views.py file for CRIM project.

This file is part of the Django Testing part of the crim application.
The testing component consists of several parts testing all the models,
views, API views, and their respective methods in order to ensure the
proper functionality of the applicaiton. Whenever an engineer implements
any major changes to the CRIM project, they should run the test suite locally
to ensure that the application architecture is maintained and all core methods
return desired results.

This specific module tests CRIM Views. Views are Python methods that configure
the displayed content based on the used objects and their properties. This file
tests their constructors and class methods.

@author: Oleh Shostak '24
@version: 1.0
@created: 7/3/22

To-do's:

-> Figure out missing views
-> Relationship, Observation, Piece: mei files
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

from rest_framework import status
from rest_framework.test import APITestCase

import re

# CRIMGenre
class GenreViewsTestCase(TestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testGenre", genre_id="testGenre")

    def test_genre_list_view(self):
        response = self.client.get(reverse("crimgenre-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "genre/genre_list.html")
        self.assertContains(response, "Genres")

    def test_genre_detail(self):
        response = self.client.get(reverse("crimgenre-detail", kwargs={'genre_id': "testGenre"}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "piece/all_piece_list.html")
        self.assertContains(response, "Pieces:")

# CRIMMass
class MassViewsTestCase(TestCase):
    def setUp(self):
        self.dummyMassGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyMass = baker.make(CRIMMass, mass_id="testMass")

    def test_mass_list_view(self):
        response = self.client.get(reverse("crimmass-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mass/mass_list.html")
        self.assertContains(response, "Masses")

    def test_mass_detail(self):
        response = self.client.get(reverse("crimmass-detail", kwargs={'mass_id': "testMass"}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "mass/mass_detail.html")
        self.assertContains(response, "Mass")

# CRIMModel
class ModelViewsTestCase(TestCase):
    def setUp(self):
        self.dummyModel = baker.make(CRIMModel)

    def test_model_list_view(self):
        response = self.client.get(reverse("crimmodel-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "piece/model_list.html")
        self.assertContains(response, "Models")

# CJObservation
class ObservationViewsTestCase(TestCase):
    def setUp(self):
        self.dummyObservationGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyObservation = baker.make(CJObservation, id=1)

    def test_observation_list_view(self):
        response = self.client.get(reverse("cjobservation-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "observation/observation_list.html")
        self.assertContains(response, "Observations")

# CRIMPerson
class PersonViewsTestCase(TestCase):
    def setUp(self):
        self.dummyPerson = baker.make(CRIMPerson, person_id=1)

    def test_person_list_view(self):
        response = self.client.get(reverse("crimperson-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_list.html")
        self.assertContains(response, "People")

    def test_person_detail(self):
        response = self.client.get(reverse("crimperson-detail", kwargs={'person_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_detail.html")
        self.assertContains(response, "1")

# CRIMPiece
class PieceViewsTestCase(TestCase):

    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, name="testGenre", genre_id="testGenre")
        self.dummyPiece = baker.make(CRIMMassMovement, title="testPiece", piece_id=1, genre=self.dummyGenre, composer=baker.make(CRIMPerson, name="testPiecePerson"))

    def test_piece_list_view(self):
        response = self.client.get(reverse("crimpiece-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "piece/all_piece_list.html")
        self.assertContains(response, "Pieces")

# CJRelationship
class RelationshipViewsTestCase(TestCase):
    def setUp(self):
        self.dummyRelationshipGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyRelationship = baker.make(CJRelationship, id=1)

    def test_relationship_list_view(self):
        response = self.client.get(reverse("cjrelationship-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "relationship/relationship_list.html")
        self.assertContains(response, "Relationships")

# CRIMRoleType
class RoleTypeViewsTestCase(TestCase):
    def setUp(self):
        self.dummyRoleType = baker.make(CRIMRoleType, role_type_id=1)

    def test_roletype_list_view(self):
        response = self.client.get(reverse("crimroletype-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "roletype/roletype_list.html")
        self.assertContains(response, "Role")

    def test_roletype_detail(self):
        response = self.client.get(reverse("crimroletype-detail", kwargs={'role_type_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "person/person_list.html")
        self.assertContains(response, "1")

#CRIMSource
class SourceViewsTestCase(TestCase):
    def setUp(self):
        self.dummySource = baker.make(CRIMSource, document_id=1)

    def test_source_list_view(self):
        response = self.client.get(reverse("crimsource-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "source/source_list.html")
        self.assertContains(response, "Source")

    def test_source_detail(self):
        response = self.client.get(reverse("crimsource-detail", kwargs={'document_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "source/source_detail.html")
        self.assertContains(response, "1")

#CRIMTreatise
class TreatiseViewsTestCase(TestCase):
    def setUp(self):
        self.dummyTreatise = baker.make(CRIMTreatise, document_id=1)

    def test_treatise_list_view(self):
        response = self.client.get(reverse("crimtreatise-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "treatise/treatise_list.html")
        self.assertContains(response, "Treatise")

    def test_treatise_detail(self):
        response = self.client.get(reverse("crimtreatise-detail", kwargs={'document_id': 1}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "treatise/treatise_detail.html")
        self.assertContains(response, "1")
