"""
This is the test_functional.py file for CRIM project.

This file is part of the Django Testing part of the CRIM application.
The testing component consists of several parts testing all the models,
views, API views, and their respective methods in order to ensure the
proper functionality of the applicaiton. Whenever an engineer implements
any major changes to the CRIM project, they should run the test suite locally
to ensure that the application architecture is maintained and all core methods
return desired results.

This specific module constitues the Functional Testing for the CRIM application.
Functional Testing mainly focuses on making sure every aspect of the web application
functions as expected by its users. Within this file, three types of users are 
outlined: Visitor, User, Admin. For each of the users, most likely and overarching 
scenarios have been desinged. These scenarios reflect the users' expected behaviors,
and mainly the pages they could visit and the actions they could perform.

@author: Oleh Shostak '24
@version: 1.0
@created: 3/7/23

To-do's:

-> User: authentication, adding and editing Observations and Relationships
-> Admin: authentication, adding and editing Observations and Relationships, 
    including other people's data

"""

import os
import random
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright
from django.urls import reverse
from rest_framework import status
import requests

class VisitorTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_landing_page(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000")
        self.assertTrue("CRIM" in page.content())
        page.close()

    def test_checkout_about_pages(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.click('a:text("About")')
        self.assertTrue(page.locator('.dropdown-menu').filter(has_text="Code").is_visible())

        # checkout the Code section
        page.click('a:text("Code")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Editions section
        page.click('a:text("About")')
        page.click('a:text("Editions")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Help section
        page.click('a:text("About")')
        page.click('a:text("Help")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Introduction section
        page.click('a:text("About")')
        page.click('a:text("Introduction")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Music section
        page.click('a:text("About")')
        page.click('a:text("Music")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Participants section
        page.click('a:text("About")')
        page.click('a:text("Participants")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Rights section
        page.click('a:text("About")')
        page.click('a:text("Rights")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Sponsors section
        page.click('a:text("About")')
        page.click('a:text("Sponsors")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)
        page.go_back()

        # checkout the Technologies section
        page.click('a:text("About")')
        page.click('a:text("Technologies")')
        self.assertTrue(len(page.locator("#home-page").text_content()) > 0)

        # conclude the test
        page.close()

    def test_checkout_masses(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/")
        page.click('a:text("Documents")')
        self.assertTrue(page.locator('.dropdown-menu').filter(has_text="Masses").is_visible())

        # navigate to Masses
        page.click('a:text("Masses")')
        self.assertFalse(page.get_by_role("heading", name="Masses").count() == 0)
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Mass)
        random_mass_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_mass_id = random_mass_row.get_by_role("link").nth(0).inner_text()
        
        # check if name link and ID link are same
        self.assertEqual(random_mass_row.get_by_role("link").nth(0).get_attribute("href"), random_mass_row.get_by_role("link").nth(1).get_attribute("href"))

        # navigate to first Mass page by ID
        random_mass_row.get_by_role("link").nth(0).click()
        random_mass_url = page.url
        self.assertTrue(random_mass_id in page.content())

        first_movement_links = page.locator("div .well").filter(has=page.get_by_role("heading").filter(has_text="Mass movements")).get_by_role("link")

        # # check downloads: PDF: FIX NEEDED
        # with page.expect_download() as download_info:
        #     first_movement_links.nth(0).click()
        #     download = download_info.value
        #     self.assertEqual(download.failure(), None)
        
        # # check downloads: MEI: FIX NEEDED
        # with page.expect_download() as download_info:
        #     first_movement_links.nth(1).click()
        #     download = download_info.value
        # #     self.assertEqual(download.failure(), None)

        # # navigate to the First Movement: configure to click()
        # page.goto(first_movement_links.nth(2).get_attribute("href"))
        # page.wait_for_selector("svg")
        # self.assertTrue(page.locator("svg").first.is_visible())
        # self.assertTrue(page.locator("#piece_score").is_visible())

        # back to Masses
        page.go_back()
        # page.go_back()

        # navigate to first Composer
        if random_mass_row.get_by_role("link").count() > 2:
            random_mass_composer_name = random_mass_row.get_by_role("link").nth(2).inner_text()
            if random_mass_composer_name.strip():
                random_mass_row.get_by_role("link").nth(2).click()
                self.assertTrue(random_mass_composer_name in page.content())

        # conclude test
        page.close()

    def test_checkout_models(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/models")
        self.assertFalse(page.get_by_role("heading", name="Models").count() == 0)
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Model)
        random_model_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_model_id = random_model_row.get_by_role("link").nth(0).inner_text()
        
        # check downloads: PDF
        with page.expect_download() as download_info:
            random_model_row.get_by_role("link").nth(0).click()
            download = download_info.value
            self.assertEqual(download.failure(), None)

        # check downloads: MEI
        with page.expect_download() as download_info:
            random_model_row.get_by_role("link").nth(1).click()
            download = download_info.value
            self.assertEqual(download.failure(), None)

        # navigate to Model by ID
        random_model_row.get_by_role("link").nth(2).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").first.is_visible())
        self.assertTrue(page.locator("#piece_score").is_visible())

        # back to Models
        page.go_back()

        # navigate to Composer
        random_model_composer_name = random_model_row.get_by_role("link").nth(3).inner_text()
        random_model_row.get_by_role("link").nth(3).click()
        self.assertTrue(random_model_composer_name in page.content())

        # back to Models
        page.go_back()

        # navigate to Genre
        random_model_genre_name = random_model_row.get_by_role("link").nth(4).inner_text()
        random_model_row.get_by_role("link").nth(4).click()
        self.assertTrue(random_model_genre_name in page.content())

        # check table contents
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # conclude test
        page.close()

    def test_checkout_pieces(self):
        page = self.browser.new_page()

        # checkout pieces
        page.goto("http://127.0.0.1:8000/pieces")
        self.assertFalse(page.get_by_role("heading", name="Pieces (all)").count() == 0)
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Piece)
        random_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))

        # check downloads: PDF
        with page.expect_download() as download_info:
            random_row.get_by_role("link").nth(0).click()
            download = download_info.value
            self.assertEqual(download.failure(), None)

        # check downloads: MEI
        with page.expect_download() as download_info:
            random_row.get_by_role("link").nth(1).click()
            download = download_info.value
            self.assertEqual(download.failure(), None)

        # navigate to Model by ID
        random_row.get_by_role("link").nth(2).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").first.is_visible())
        self.assertTrue(page.locator("#piece_score").is_visible())

        # back to Pieces
        page.go_back()

        # check out random Composer
        random_composer_name = random_row.get_by_role("link").nth(3).inner_text()
        random_row.get_by_role("link").nth(3).click()
        self.assertTrue(random_composer_name in page.content())

        # back to Pieces
        page.go_back()

        # check out random Genre
        random_genre_name = random_row.get_by_role("link").nth(4).inner_text()
        random_row.get_by_role("link").nth(4).click()
        self.assertTrue(random_genre_name in page.content())
        self.assertTrue(page.locator("table").count() > 0)

        # back to Pieces
        page.go_back()

        # check out the list of genres
        page.click('a:text("list of genres")')
        self.assertTrue(page.locator("table").count() > 0)

        # conclude test
        page.close()

    def test_checkout_sources(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/sources")
        self.assertFalse(page.get_by_role("heading", name="Sources").count() == 0)
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Piece)
        random_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))

        # checking source link: FIX NEEDED
        # random_row.get_by_role("link").nth(1).click()
        # with sync_playwright() as p:
        #     source_page = self.browser.new_page()
        #     response = page.goto(random_row.get_by_role("link").nth(1).get_attribute("href"))
        #     print(response.status)
        #     page.close()

        # check source CRIM page:
        souce_id = random_row.get_by_role("link").nth(1).inner_text()
        random_row.get_by_role("link").nth(1).click()
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(souce_id in page.content())

        # back to sources
        page.go_back()

        # check source author page: FIX NEEDED
        # souce_author = random_row.get_by_role("link").nth(2).inner_text()
        # random_row.get_by_role("link").nth(2).click()
        # self.assertTrue(page.locator("table").count() > 0)
        # self.assertTrue(souce_author in page.content())

        # conclude test
        page.close()

    def test_checkout_people(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/people")

        # check table
        self.assertFalse(page.get_by_role("heading", name="People").count() == 0)
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Person)
        random_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))

        # checkout random Person
        random_person_id = random_row.get_by_role("link").nth(0).inner_text()
        random_row.get_by_role("link").nth(0).click()
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(random_person_id in page.content())

        # back to People
        page.go_back()

        # checkout people with the same role (if any)
        if random_row.get_by_role("link").count() > 1:
            random_row.get_by_role("link").nth(1).click()
            self.assertTrue(page.locator("table").count() > 0)
            self.assertTrue(page.locator("tr").count() >= 2)

        # back to People
        page.go_back()

        # check out the list of role types
        page.click('a:text("list of role types")')
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # conclude the test
        page.close()

    def test_checkout_observations(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000")
        page.click('a:text("Analysis")')
        self.assertTrue(page.locator('.dropdown-menu').filter(has_text="Observations").is_visible())

        # navigate to Observations
        page.click('a:text("Observations")')
        self.assertFalse(page.get_by_role("heading", name="Observations").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Observation)
        random_observation_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_observation_id = random_observation_row.get_by_role("link").nth(0).inner_text()

        # navigate to Observation by ID
        random_observation_row.get_by_role("link").nth(0).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").first.is_visible())
        self.assertTrue(page.locator("#observation_score").is_visible())

        # back to Observations:
        page.go_back()

        # navigate to Observer
        random_observer_name = random_observation_row.get_by_role("link").nth(1).inner_text()
        random_observation_row.get_by_role("link").nth(1).click()
        page.wait_for_selector("table")
        self.assertTrue(random_observer_name in page.content())
        self.assertTrue(page.locator("table").count() > 0)

        # back to Observations
        page.go_back()

        # navigate to Observation by ID
        random_observation_row.get_by_role("link").nth(2).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").first.is_visible())
        self.assertTrue(page.locator("#piece_score").is_visible())

        # conclude test
        page.close()

    def test_checkout_relationships(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/relationships")

        # check if table is present
        self.assertFalse(page.get_by_role("heading", name="Relationships").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Relationship)
        random_relationship_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_relationship_id = random_relationship_row.get_by_role("link").nth(0).inner_text()

        # navigate to Relationship by ID
        random_relationship_row.get_by_role("link").nth(0).click()
        page.wait_for_selector("svg")

        # check model score and scale
        self.assertTrue(page.locator("svg").nth(0).is_visible())
        self.assertTrue(page.locator("svg").nth(1).is_visible())

        # check Derivative score and scale
        self.assertTrue(page.locator("svg").nth(2).is_visible())
        self.assertTrue(page.locator("svg").nth(3).is_visible())

        # check for text contents:
        self.assertTrue("Model" in page.content())
        self.assertTrue("Derivative" in page.content())
        self.assertTrue("Observer" in page.content())

        # back to Relationships 
        page.go_back()

        # navigate to random Observer
        random_observer_name = random_relationship_row.get_by_role("link").nth(1).inner_text()
        random_relationship_row.get_by_role("link").nth(1).click()
        self.assertTrue(random_observer_name in page.content())
        self.assertTrue(page.locator("table").count() > 0)

        # back to Relationships
        page.go_back()

        # navigate to Model observation
        random_relationship_row.get_by_role("link").nth(2).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").nth(0).is_visible())
        self.assertTrue(page.locator("svg").nth(1).is_visible())
        self.assertTrue(page.locator("#observation_score").is_visible())

        # back to Relationships
        page.go_back()

        # navigate to Model Piece
        random_relationship_row.get_by_role("link").nth(3).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").nth(0).is_visible())
        self.assertTrue(page.locator("svg").nth(1).is_visible())
        self.assertTrue(page.locator("#piece_score").is_visible())

        # back to Relationships
        page.go_back()

        # navigate to Derivative observation
        random_relationship_row.get_by_role("link").nth(4).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").nth(0).is_visible())
        self.assertTrue(page.locator("svg").nth(1).is_visible())
        self.assertTrue(page.locator("#observation_score").is_visible())

        # back to Relationships
        page.go_back()

        # navigate to Derivative Piece
        random_relationship_row.get_by_role("link").nth(5).click()
        page.wait_for_selector("svg")

        # check if SVG is visible
        self.assertTrue(page.locator("svg").nth(0).is_visible())
        self.assertTrue(page.locator("svg").nth(1).is_visible())
        self.assertTrue(page.locator("#piece_score").is_visible())

        # conclude test
        page.close()

    def test_checkout_forum(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/")

        # navigate to Forum
        page.click('a:text("Forum")')

        # check table
        self.assertFalse(page.get_by_role("heading", name="Forum").count() == 0)
        self.assertTrue(page.locator("table").count() > 0)

        # try to navigate to new discussion:
        page.locator("a").filter(has=page.locator("button").filter(has_text="New discussion")).click()

        # check if login required
        self.assertTrue("Username:" in page.content())
        self.assertTrue("Password:" in page.content())

        # conclude test
        page.close()

class UserTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_landing_page(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000")
        self.assertTrue("CRIM" in page.content())
        page.close()

class AdminTestCase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def test_landing_page(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/")
        self.assertTrue("CRIM" in page.content())
        page.close()