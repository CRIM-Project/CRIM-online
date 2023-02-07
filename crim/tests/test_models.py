"""
This is the test_models.py file for CRIM project.

This file is part of the Django Testing part of the crim application.
The testing component consists of several parts testing all the models,
views, API views, and their respective methods in order to ensure the
proper functionality of the applicaiton. Whenever an engineer implements
any major changes to the CRIM project, they should run the test suite locally
to ensure that the application architecture is maintained and all core methods
return desired results.

This specific module tests CRIM Models. Models are Python objects that outline
the most common/standard classes used by the application. This file tests their
constructors and class methods.

@author: Oleh Shostak '24
@version: 1.0
@created: 7/3/22


To-do's:

-> test save (for a bunch of classes)
-> CRIMNote (__str__) not working (rewrite the original CRIMNote method)
"""

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
from rest_framework.test import force_authenticate


import re

# CRIMPerson
class PersonTestCase(TestCase):
    def setUp(self):
        self.dummyPerson = mixer.blend(CRIMPerson)

    def test_sorted_name(self):
        self.assertEqual(self.dummyPerson.name_sort, self.dummyPerson.sorted_name())

    def test_get_absolute_url(self):
        self.assertEqual(self.dummyPerson.get_absolute_url(), '/people/' + self.dummyPerson.person_id + '/')

    def test_self_string(self):
        self.assertEqual(str(self.dummyPerson), self.dummyPerson.name_sort)

# CRIMDefinition
class DefinitionTestCase(TestCase):
    def setUp(self):
        self.dummyDefinition = baker.make(CRIMDefinition)

    def test_self_string(self):
        self.assertEqual(str(self.dummyDefinition), str(self.dummyDefinition.pk))

# CRIMSource, CRIMTreatise
class SourceTestCase(TestCase):
    def setUp(self):
        self.dummySource = mixer.blend(CRIMSource)
        self.dummyTreatise = mixer.blend(CRIMTreatise)

    def test_title_with_id(self):
        self.assertEqual(self.dummySource.title_with_id(), str(self.dummySource))
        self.assertEqual(self.dummyTreatise.title_with_id(), str(self.dummyTreatise))

    def test_clean(self):
        self.incorrectSource = mixer.blend(CRIMSource, document_id="%%332")
        self.incorrectTreatise = mixer.blend(CRIMTreatise, document_id="%%333")

        with self.assertRaises(ValidationError):
            self.incorrectSource.clean()

        with self.assertRaises(ValidationError):
            self.incorrectTreatise.clean()

    def test_self_string(self):
        self.assertTrue(self.dummySource.title in str(self.dummySource))
        self.assertTrue(self.dummyTreatise.document_id in str(self.dummyTreatise))

    def test_get_absolute_url(self):
        self.assertEqual(self.dummySource.get_absolute_url(), '/sources/' + self.dummySource.document_id + '/')
        self.assertEqual(self.dummyTreatise.get_absolute_url(), '/treatises/' + self.dummyTreatise.document_id + '/')

    # test save()

# CRIMForumPost
class ForumTestCase(TestCase):
    def setUp(self):
        self.dummyForum = baker.make(CRIMForumPost, post_id=1, author=baker.make(CRIMUserProfile, person=baker.make(CRIMPerson)))

    def test_string_self(self):
        self.assertTrue(self.dummyForum.author.name in str(self.dummyForum))

    def test_get_unique_slug(self):
        self.assertTrue(self.dummyForum.author.user.username in self.dummyForum._get_unique_slug())

    # test save(), get_absolute_url()

# CRIMGenre
class GenreTestCase(TestCase):
    def setUp(self):
        self.dummyGenre = mixer.blend(CRIMGenre)

    def test_string_self(self):
        self.assertEqual(self.dummyGenre.name, str(self.dummyGenre))

    def test_get_unique_slug(self):
        self.assertTrue(slugify(self.dummyGenre.name) in self.dummyGenre._get_unique_slug())

# CRIMMass
class MassTestCase(TestCase):
    def setUp(self):
        self.dummyMassGenre = mixer.blend(CRIMGenre, genre_id="mass")
        self.dummyMass = mixer.blend(CRIMMass)

    def test_title_with_id(self):
        self.assertEqual(self.dummyMass.title_with_id(), str(self.dummyMass))

    def test_string_self(self):
        self.assertTrue(self.dummyMass.title in str(self.dummyMass))
        self.assertTrue(self.dummyMass.mass_id in str(self.dummyMass))

    def test_clean(self):
        self.incorrectMass = mixer.blend(CRIMMass, mass_id="%%33222")

        with self.assertRaises(ValidationError):
            self.incorrectMass.clean()

    def test_get_absolute_url(self):
        self.assertEqual(self.dummyMass.get_absolute_url(), '/masses/' + self.dummyMass.mass_id + '/')

# CRIMNote
class NoteTestCase(TestCase):
    def setUp(self):
        self.dummyNote = baker.make(CRIMNote, author=baker.make(CRIMUserProfile, person=baker.make(CRIMPerson, name="testNotePerson", name_sort="testNotePerson")))

    def test_string_self(self):
        self.assertTrue(isinstance(str(self.dummyNote), str))

# CJObservation
class ObservationTestCase(TestCase):
    def setUp(self):
        self.dummyMassGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyObservation = baker.make(CJObservation)

    def test_get_absolute_url(self):
        self.assertEqual(self.dummyObservation.get_absolute_url(), '/observations/' + str(self.dummyObservation.pk) + '/')

    def test_string_self(self):
        self.assertTrue(str(self.dummyObservation.id) in str(self.dummyObservation))

    def test_id_in_brackets(self):
        self.assertTrue(str(self.dummyObservation.id) in self.dummyObservation.id_in_brackets())

# testing Part
class PartTestCase(TestCase):
    def setUp(self):
        self.dummyPartGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyPart = baker.make(CRIMPart, piece=baker.make(CRIMPiece))

    def test_title(self):
        self.assertTrue(self.dummyPart.piece.title in self.dummyPart.piece_title())

    def test_string_self(self):
        self.assertTrue(str(self.dummyPart.part_id) in str(self.dummyPart))

    # test save

# CRIMPhrase
class PhraseTestCase(TestCase):
    def setUp(self):
        self.dummyPhraseGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyPhrase = baker.make(CRIMPhrase, part=baker.make(CRIMPart, piece=baker.make(CRIMPiece)))

    def test_title(self):
        self.assertTrue(self.dummyPhrase.piece.title in self.dummyPhrase.piece_title())

    def test_string_self(self):
        self.assertTrue(self.dummyPhrase.phrase_id in str(self.dummyPhrase))
        self.assertTrue(self.dummyPhrase.piece.title in str(self.dummyPhrase))
        self.assertTrue(str(self.dummyPhrase.number) in str(self.dummyPhrase))

    def test_part_number(self):
        self.assertEqual(self.dummyPhrase.part_number(), self.dummyPhrase.part.order)

    # test save

# Mass Movement / Model
class MassMovementTestCase(TestCase):
    def setUp(self):
        self.dummyMassMovement = baker.make(CRIMMassMovement)

    def test_title_with_id(self):
        self.assertEqual(str(self.dummyMassMovement), self.dummyMassMovement.title_with_id())

    def test_get_absolute_url(self):
        self.assertEqual(self.dummyMassMovement.get_absolute_url(), '/pieces/' + str(self.dummyMassMovement.piece_id) + '/')

    def test_clean(self):
        self.dummyGenre = baker.make(CRIMGenre, genre_id="mass")
        self.incorrectMassMovement = baker.make(CRIMMassMovement, piece_id="&^*^*&")

        with self.assertRaises(ValidationError):
            self.incorrectMassMovement.clean()

    # test save

# CJRelationship
class RelationshipTestCase(TestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyRelationship = baker.make(CJRelationship, observer=baker.make(CRIMPerson), model_observation=baker.make(CJObservation), derivative_observation=baker.make(CJObservation), definition=baker.make(CRIMDefinition), model_piece=baker.make(CRIMPiece), derivative_piece=baker.make(CRIMPiece))

    def test_id_in_brackets(self):
        self.assertTrue(isinstance(self.dummyRelationship.id_in_brackets(), str))

    def test_get_absolute_url(self):
        self.assertEqual(self.dummyRelationship.get_absolute_url(), '/relationships/' + str(self.dummyRelationship.pk) + '/')

    def test_string_self(self):
        self.assertTrue(self.dummyRelationship.id_in_brackets() in str(self.dummyRelationship))

    # test save

# CRIMRoleType
class RoleTypeTestCase(TestCase):
    def setUp(self):
        self.dummyRoleType = baker.make(CRIMRoleType)

    def test_get_unique_slug(self):
        self.assertTrue(slugify(self.dummyRoleType.name) in self.dummyRoleType._get_unique_slug())

    def test_self_string(self):
        self.assertEqual(str(self.dummyRoleType), self.dummyRoleType.name)

    # test save

# CRIMRole
class RoleTestCase(TestCase):
    def setUp(self):
        self.dummyRole = baker.make(CRIMRole, person=baker.make(CRIMPerson), role_type=baker.make(CRIMRoleType))

    def test_self_string(self):
        self.assertTrue(str(self.dummyRole.person) in str(self.dummyRole))

    def test_person_with_role(self):
        self.assertTrue(str(self.dummyRole.person) in self.dummyRole.person_with_role())

    def test_clean(self):
        self.dummyGenre = baker.make(CRIMGenre, genre_id="mass")
        self.incorrectRole = baker.make(CRIMRole, treatise=baker.make(CRIMTreatise), mass=baker.make(CRIMMass))

        with self.assertRaises(ValidationError):
            self.incorrectRole.clean()

    # test Save

# CRIMUserProfile
class UserTestCase(TestCase):
    def setUp(self):
        self.dummyUser = baker.make(CRIMUserProfile, person=baker.make(CRIMPerson), name="USERNAME")

    def test_string_self(self):
        self.incorrectUser = baker.make(CRIMUserProfile, person=baker.make(CRIMPerson, name="TESTNAME"), name=False)
        self.assertEqual(str(self.dummyUser), self.dummyUser.name)
        self.assertTrue(str(self.incorrectUser), self.incorrectUser.user.username)

# CRIMVoice
class VoiceTestCase(TestCase):
    def setUp(self):
        self.dummyGenre = baker.make(CRIMGenre, genre_id="mass")
        self.dummyVoiceMass = baker.make(CRIMMass)
        self.dummyVoiceMassMovement = baker.make(CRIMModel)
        self.dummyVoice = baker.make(CRIMVoice, piece=self.dummyVoiceMassMovement)

    def test_piece_title(self):
        if self.dummyVoice.piece.mass == None:
            self.assertEqual(self.dummyVoice.piece_title(), self.dummyVoice.piece.title)

    def test_string_self(self):
        self.assertTrue(str(self.dummyVoice.order) in str(self.dummyVoice))
        self.assertTrue(str(self.dummyVoice.regularized_name) in str(self.dummyVoice))

    def test_clean(self):
        self.incorrectVoice = baker.make(CRIMVoice, piece=baker.make(CRIMMassMovement, piece_id="%%%$#$"), clef="%%%$#$")

        with self.assertRaises(ValidationError):
            self.incorrectVoice.clean()

    # test save
