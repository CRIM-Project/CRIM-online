# This is the Read Me file for the Testing portion of the CRIM project.

The files in the Testing folder outline several Testing procedures necessary to ensure that the CRIM 
application works as expected. Mainly, they are as follows:

1. **test_models.py** <br><br>
    This file constitutes a Testing suite for the Django's Python Models for CRIM. Models are
    the objects that CRIM's system relies upon – and mainly constitue the important Object classes that 
    define the key actors and elements in the CRIM applicaiton. Within this file, we test:
    - CRIMPerson
    - CRIMDefinition
    - CRIMSource
    - CRIMTreatise
    - CRIMForumPost
    - CRIMGenre
    - CRIMMass
    - CRIMNote
    - CJObservation
    - CRIMPart
    - CRIMPhrase
    - CRIMMassMovement
    - CJRelationship
    - CRIMRoleType
    - CRIMRole
    - CRIMUserProfile
    - CRIMVoice
    
The specific things that could be improved within this file are:
+ test save (for a bunch of classes)
+ CRIMNote (__str__) not working (rewrite the original CRIMNote method)


-----
    
2. **test_views.py** <br><br>
    This file constitutes a Testing suite for the Django's Python Views for CRIM. Views are
    the methods that CRIM's system relies upon – and mainly constitue the important functions that
    deliver and arrange the data, HTML templates, and URLs for all CRIM prages. Within this file, we test:
    - CRIMGenre: list, detail
    - CRIMMass: list, detail
    - CRIMModel: list
    - CJObservation: list
    - CRIMPerson: list, detail
    - CRIMPiece: list
    - CJRelationship: list
    - CRIMRoleType: list, detail
    - CRIMSource: list, detail
    - CRIMTreatise: list, detail

The specific things that could be improved within this file are:
+ Figure out missing views
+ Relationship, Observation, Piece: mei files

------

3. **test_API_views.py** <br> <br>
    This file constitutes a Testing suite for the CRIM API's Python Views, used to serve data. The API Views are
    the methods that CRIM's API uses to performe delivery, arrangement, and CRUD operations on the CRIM objects. Within this file, we test:
    - CRIMGenre: list, detail
    - CRIMMass: list, detail
    - CRIMModel: list
    - CJObservation: list, brief list, detail, new observation
    - CRIMPart: list, detail
    - CRIMPerson: list, detail
    - CRIMPhrase: list, detail
    - CRIMPiece: list, detail, relationship detail
    - CJRelationship: list, brief list, detail, new relationship
    - CRIMRole: list, detail
    - CRIMRoleType: list, detail
    - CRIMSource: list, detail
    - CRIMTreatise: list, detail
    - CRIMVoice: list, detail

The specific things that could be improved within this file are:
+ CRIMDefinition (id parameter doesn't work)
+ Relationship (figure out list serializer)


------

4. **test_functional.py** <br><br>
    This specific module constitues the Functional Testing for the CRIM application. Functional Testing mainly focuses on making sure every aspect of the web application functions as expected by its users. Within this file, three types of users are outlined: Visitor, User, Admin. For each of the users, most likely and overarching scenarios have been desinged. These scenarios reflect the users' expected behaviors, and mainly 
    the pages they could visit and the actions they could perform. Within this file, we test:
    - **@Visitor**
        - test_landing_page: checking out landing page
        - test_checkout_about_pages: looking at all about pages
        - test_checkout_masses: looking at a random Mass
        - test_checkout_models: looking at a random Model
        - test_checkout_pieces: looking at a random Piece
        - test_checkout_sources: looking at a random Source
        - test_checkout_people: looking at a random Person
        - test_checkout_observations: looking at a random Observation
        - test_checkout_relationships: looking at a random Relationship
        - test_checkout_forum: checking out forum
    - **@User**
        - test_landing_page: checking out landing page
    - **@Admin**
        - test_landing_page: checking out landing page

The specific things that could be improved within this file are:
+ @User: authentication, adding and editing Observations and Relationships
+ @Admin: authentication, adding and editing Observations and Relationships, including other people's data


-----
-----

# GitHub Workflow

The testing process is automated as part of a CI/CD process, hosted using GitHub Actions. The process of executing 
the tests is outlined in the crim-test.yml file, and mainly follows these steps:

1. Checkout the Code
2. Set up Python
3. Install Dependencies
4. Set up the CRIM app
5. Test Models
6. Test Views
7. Test API Views
8. Clear data and load fixtures
9. Functional Testing
10. Flake8 testing
11. Conclude testing