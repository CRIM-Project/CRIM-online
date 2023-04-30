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
@version: 2.0
@created: 4/30/23

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
        cls.trace = False

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def c_print(self, string_input):
        if self.trace:
            print(string_input)
        else: 
            pass

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
        page.wait_for_selector("table")
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

        # get random movement
        page.wait_for_selector("a")
        movement_headings = page.locator("div .well").filter(has=page.get_by_role("heading").filter(has_text="Mass movements")).locator("h3")
        random_movement_links = movement_headings.nth(random.randint(0, movement_headings.count() - 1)).locator("a")
        movement_mei_included = False

        # iterate over the links for a random movement
        for i in range(random_movement_links.count()):

            # storing the link
            local_link = random_movement_links.nth(i)
            local_link_url = local_link.get_attribute("href")

            # MEI link:
            if local_link_url.endswith(".mei"):
                movement_mei_included = True

                # just in case there is an unregistered missing MEI mass movement
                self.c_print("\n Downloading MEI for Mass Movement: \n" + local_link_url + "\n")

                # test MEI file download:
                with page.expect_download() as download_info:
                    local_link.click()
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith('.mei'))
                download.delete()
            
            # PDF link:
            elif local_link_url.endswith(".pdf"):
                
                # just in case there is an unregistered missing PDF mass movement
                self.c_print("\n Downloading PDF for Mass Movement: \n" + local_link_url + "\n")

                # test PDF file download:
                with page.expect_download() as download_info:
                    local_link.click(modifiers=["Alt"])
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith('.pdf'))
                download.delete()

            # Piece link:  
            elif "piece" in local_link_url:
                page.wait_for_selector("a")
                page.goto(local_link_url)

                # if there is an MEI file, we should see the score:
                if movement_mei_included:
                    page.wait_for_selector("svg")

                    # check if SVG is visible
                    self.assertTrue(page.locator("svg").first.is_visible())
                    self.assertTrue(page.locator("#piece_score").is_visible())

                # go back
                page.go_back()

        # back to Masses
        page.go_back()

        # navigate to first Composer
        if random_mass_row.get_by_role("link").count() > 2:
            random_mass_composer_name = random_mass_row.get_by_role("link").nth(2).inner_text()
            if random_mass_composer_name.strip():
                random_mass_row.get_by_role("link").nth(2).click()
                self.assertTrue(random_mass_composer_name in page.content())

        # conclude test
        page.close()

    def test_checkout_models(self):

        # nagigating to and checking out the Models table
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/models")
        self.assertFalse(page.get_by_role("heading", name="Models").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Model)
        random_model_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_model_links = random_model_row.get_by_role("link")
        model_mei_included = False

        # iterating over the Model links
        for i in range(random_model_links.count()):
            
            # storing the link
            local_link = random_model_links.nth(i)
            local_link_url = local_link.get_attribute("href")
            
            # MEI link:
            if local_link_url.endswith(".mei"):
                model_mei_included = True

                # just in case there is an unregistered missing MEI model
                self.c_print("\n Downloading MEI for Model: \n" + local_link_url + "\n")

                # test MEI file download:
                with page.expect_download() as download_info:
                    local_link.click()
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith('.mei'))
                download.delete()

            # PDF link:
            elif local_link_url.endswith(".pdf"):
                
                # just in case there is an unregistered missing PDF model
                self.c_print("\n Downloading PDF for Model: \n" + local_link_url + "\n")

                # test PDF file download:
                with page.expect_download() as download_info:
                    local_link.click(modifiers=["Alt"])
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith('.pdf'))
                download.delete()

            # Piece link:  
            elif "piece" in local_link_url:

                # just for tracking purposes
                self.c_print("\n Working with Model: \n" + local_link_url + "\n")

                page.wait_for_selector("a")
                page.goto(local_link_url)

                # if there is an MEI file, we should see the score:
                if model_mei_included:
                    page.wait_for_selector("svg")

                    # check if SVG is visible
                    self.assertTrue(page.locator("svg").first.is_visible())
                    self.assertTrue(page.locator("#piece_score").is_visible())

                # go back
                page.go_back()

            # People link
            elif "people" in local_link_url:
                
                # record composer name:
                random_model_composer_name = local_link.inner_text()

                # navigate to link
                page.goto(local_link_url)

                # check if composer name is present
                self.assertTrue(random_model_composer_name in page.content())
                
                # back to models
                page.go_back()

            # Genre link
            elif "genre" in local_link_url:

                # record genre name
                random_model_genre_name = local_link.inner_text()

                # navigate to the genre page
                page.goto(local_link_url)

                # cehck for genre name
                self.assertTrue(random_model_genre_name in page.content())

                # check table contents
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)

                # back to Models
                page.go_back()

        # conclude test
        page.close()

    def test_checkout_pieces(self):
        page = self.browser.new_page()

        # navigate to and checkout the Pieces table
        page.goto("http://127.0.0.1:8000/pieces")
        self.assertFalse(page.get_by_role("heading", name="Pieces (all)").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Piece)
        random_piece_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_piece_links = random_piece_row.get_by_role("link")
        piece_mei_included = False

        # iterating over the Piece links
        for i in range(random_piece_links.count()):
            
            # storing the link
            local_link = random_piece_links.nth(i)
            local_link_url = local_link.get_attribute("href")
            
            # MEI link:
            if local_link_url.endswith(".mei"):
                piece_mei_included = True

                # just in case there is an unregistered missing MEI Piece
                self.c_print("\n Downloading MEI for Piece: \n" + local_link_url + "\n")

                # test MEI file download:
                with page.expect_download() as download_info:
                    local_link.click()
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith('.mei'))
                download.delete()

            # PDF link:
            elif local_link_url.endswith(".pdf"):
                
                # just in case there is an unregistered missing PDF piece
                self.c_print("\n Downloading PDF for Piece: \n" + local_link_url + "\n")

                # test PDF file download:
                with page.expect_download() as download_info:
                    local_link.click(modifiers=["Alt"])
                download = download_info.value
                self.assertTrue(download.suggested_filename.endswith('.pdf'))
                download.delete()

            # Piece link:  
            elif "piece" in local_link_url:

                # just for tracking purposes
                self.c_print("\n Working with Piece: \n" + local_link_url + "\n")

                page.wait_for_selector("a")
                page.goto(local_link_url)

                # if there is an MEI file, we should see the score:
                if piece_mei_included:
                    page.wait_for_selector("svg")

                    # check if SVG is visible
                    self.assertTrue(page.locator("svg").first.is_visible())
                    self.assertTrue(page.locator("#piece_score").is_visible())

                # go back
                page.go_back()

            # People link
            elif "people" in local_link_url:
                
                # record composer name:
                random_piece_composer_name = local_link.inner_text()

                # navigate to link
                page.goto(local_link_url)

                # check if composer name is present
                self.assertTrue(random_piece_composer_name in page.content())
                
                # back to Pieces
                page.go_back()

            # Genre link
            elif "genre" in local_link_url:

                # record genre name
                random_piece_genre_name = local_link.inner_text()

                # navigate to the genre page
                page.goto(local_link_url)

                # cehck for genre name
                self.assertTrue(random_piece_genre_name in page.content())

                # check table contents
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)

                # back to Pieces
                page.go_back()

        # check out the list of genres
        page.click('a:text("list of genres")')
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)

        # conclude test
        page.close()

    def test_checkout_sources(self):

        # navigate and checkout the sources table
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/sources")
        self.assertFalse(page.get_by_role("heading", name="Sources").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Source)
        random_source_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_source_links = random_source_row.locator("a")

        # iterating over the Source links
        for i in range(random_source_links.count()):
            
            # storing the link
            local_link = random_source_links.nth(i)
            local_link_url = local_link.get_attribute("href")
            
            # CRIM Sources link
            if "sources" in local_link_url:

                # store source ID
                random_source_id = local_link.inner_text()

                # just for tracking purposes
                self.c_print("\n Working with Source: \n" + local_link_url + "\n")

                page.wait_for_selector("a")
                page.goto(local_link_url)

                # check for source ID
                self.assertTrue(random_source_id in page.content())

                # check table contents
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)

                # back to Pieces
                page.go_back()

            # People link
            elif "people" in local_link_url:
                
                # record author name:
                random_source_author = local_link.inner_text()

                # navigate to link
                page.goto(local_link_url)

                # check if author's name is present
                self.assertTrue(random_source_author in page.content())
                
                # back to Pieces
                page.go_back()
            
            # EXTERNAL link: optional
            elif ("crim" not in local_link_url) and ("sources" not in local_link_url) and ("people" not in local_link_url):

                # just for tracking purposes
                self.c_print("\n Tracking external source: \n" + local_link_url + "\n")
                
                # checkout if page is up:
                response = page.goto(local_link_url)
                page.wait_for_selector("a")
                self.assertEqual(response.status, 200)

                # back to Sources:
                page.go_back()

        # conclude test
        page.close()

    def test_checkout_people(self):

        # navigate to and checkout the People table
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/people")
        self.assertFalse(page.get_by_role("heading", name="People").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Person)
        random_person_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_person_links = random_person_row.locator("a")

        # iterating over the Person links
        for i in range(random_person_links.count()):
            
            # storing the link
            local_link = random_person_links.nth(i)
            local_link_url = local_link.get_attribute("href")
            
            # Person link
            if "Person" in local_link_url:
                
                # record person ID:
                random_person_ID = local_link.inner_text()

                # navigate to link
                page.goto(local_link_url)

                # check if ID is present
                self.assertTrue(random_person_ID in page.content())

                # check table contents
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)

                # back to People
                page.go_back()
            
            # Role link
            elif "role" in local_link_url:

                # record person ID:
                random_person_role = local_link.inner_text()
    
                # navigate: 
                local_link.click()

                # check if role is present
                self.assertTrue(random_person_role in page.content())

                # check table contents
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)

                # back to People
                page.go_back()

        # conclude test
        page.close()

    def test_checkout_observations(self):

        # navigating to and checking out the observations table:
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
        random_observation_links = random_observation_row.locator("a")

        # iterating over the Observation links
        for i in range(random_observation_links.count()):
            
            # storing the link
            local_link = random_observation_links.nth(i)
            local_link_url = local_link.get_attribute("href")
            
            # Observations link:
            if "observations" in local_link_url:

                # navigate
                page.wait_for_selector("a")
                page.goto(local_link_url)
                
                # check if SVG is visible
                page.wait_for_selector("svg")
                self.assertTrue(page.locator("svg").first.is_visible())
                self.assertTrue(page.locator("#observation_score").is_visible())

                # back to Observations:
                page.go_back()
            
            # People link
            elif "people" in local_link_url:
                
                # record composer name:
                random_observer_name = local_link.inner_text()

                # navigate to link
                page.goto(local_link_url)

                # check if composer name is present
                self.assertTrue(random_observer_name in page.content())

                # check if there's at least one table:
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)
                
                # back to Relationships
                page.go_back()

            # Piece link:  
            elif "piece" in local_link_url:

                # just for tracking purposes
                self.c_print("\n Working with Observation Model: \n" + local_link_url + "\n")

                # navigate
                page.wait_for_selector("a")
                page.goto(local_link_url)
                
                # check if SVG is visible
                page.wait_for_selector("svg")
                self.assertTrue(page.locator("svg").first.is_visible())
                self.assertTrue(page.locator("#piece_score").is_visible())

                # go back
                page.go_back()

            # expander link:
            elif "#" in local_link_url:
                pass

        # conclude test
        page.close()

    def test_checkout_relationships(self):

        # navigate to and checkout the relationships table:
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/relationships")
        self.assertFalse(page.get_by_role("heading", name="Relationships").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)
        self.assertTrue(page.locator("tr").count() >= 2)

        # pick a random row (Relationship)
        random_relationship_row = page.locator("tbody").get_by_role("row").nth(random.randint(0, page.locator("tbody").get_by_role("row").count() - 1))
        random_relationship_links = random_relationship_row.locator("a")

        # iterating over the Relationship links
        for i in range(random_relationship_links.count()):
            
            # storing the link
            local_link = random_relationship_links.nth(i)
            local_link_url = local_link.get_attribute("href")

            # Relationship link:
            if "relationships" in local_link_url:

                # navigate
                page.wait_for_selector("a")
                page.goto(local_link_url)
                
                # check if SVG is visible
                page.wait_for_selector("svg")

                # check Model score and scale
                self.assertTrue(page.locator("svg").nth(0).is_visible())
                self.assertTrue(page.locator("svg").nth(1).is_visible())

                # check Derivative score and scale
                self.assertTrue(page.locator("svg").nth(2).is_visible())
                self.assertTrue(page.locator("svg").nth(3).is_visible())

                # check for text contents:
                self.assertTrue("Model" in page.content())
                self.assertTrue("Derivative" in page.content())
                self.assertTrue("Observer" in page.content())

                # back to Relationships:
                page.go_back()
            
            # People link
            elif "people" in local_link_url:
                
                # record composer name:
                random_observer_name = local_link.inner_text()

                # navigate to link
                page.goto(local_link_url)

                # check if composer name is present
                self.assertTrue(random_observer_name in page.content())

                # check if there's at least one table:
                page.wait_for_selector("table")
                self.assertTrue(page.locator("table").count() > 0)
                self.assertTrue(page.locator("tr").count() >= 2)
                
                # back to Relationships
                page.go_back()

            # Observation link:
            elif "observations" in local_link_url:

                # navigate
                page.wait_for_selector("a")
                page.goto(local_link_url)
                
                # check if SVG is visible
                page.wait_for_selector("svg")
                self.assertTrue(page.locator("svg").first.is_visible())
                self.assertTrue(page.locator("#observation_score").is_visible())

                # back to Relationships:
                page.go_back()

            # Piece link:  
            elif "piece" in local_link_url:

                # record piece name:
                local_piece_name = local_link.inner_text()

                # just for tracking purposes
                self.c_print("\n Working with Relationship Piece: \n" + local_link_url + "\n")

                # navigate
                page.wait_for_selector("a")
                page.goto(local_link_url)
                
                # check if SVG is visible
                page.wait_for_selector("svg")
                self.assertTrue(page.locator("svg").first.is_visible())
                self.assertTrue(page.locator("#piece_score").is_visible())

                # check if piece name is present:
                self.assertTrue(local_piece_name in page.content())

                # go back
                page.go_back()

            # expander link:
            elif "#" in local_link_url:
                pass
            
        # conclude test
        page.close()

    def test_checkout_forum(self):
        page = self.browser.new_page()
        page.goto("http://127.0.0.1:8000/")

        # navigate to Forum
        page.click('a:text("Forum")')

        # check table
        self.assertFalse(page.get_by_role("heading", name="Forum").count() == 0)
        page.wait_for_selector("table")
        self.assertTrue(page.locator("table").count() > 0)

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