HOWTO: CRIMOnline local development setup
------
1. Clone the repository to your local environment
2. Create a virtual environment for the project
  - Excute `python3 -m venv venv`
  - NOTE: The second `venv` is the name of the directory the virtual environment will be installed into
3. Activate the virtual environment
  - Execute `source venv/bin/activate`
  - **NOTE: When working with the project you will need to activate the virtual environment each time you open a new console**
4. Open the `requirements.txt` for editing and comment out the `psycopg2` package prefixing the line with the `#` character.
5. Install the project requirements within the virtual environment
  - Execute `pip install -r requirements.txt`
5. Copy or symbolicly link the file `crim/settings_development.py` to `crim/settings_production.py`
6. Create the django database migrations (this will generate the database model descriptions)
  - Execute `python3 ./manage.py makemigrations`
7. Migrate the django models to the database (this will create the tables in the database)
  - Execute `python3 ./manage.py migrate`
  
8. Load a recent data dump for some local test data (NOTE: Data must be imported in the exact order)
  - python3 ./manage.py loaddata <filename>
  - crim/fixtures/data-2020/1.json
  - crim/fixtures/data-2020/2.json
  - crim/fixtures/data-2020/3.json
  - crim/fixtures/data-2020/4.json
  - crim/fixtures/data-2020/5.json
  - crim/fixtures/data-2020/6.json
  - crim/fixtures/data-2020/7.json
  - crim/fixtures/data-2020/8.json
  - crim/fixtures/data-2022/definitions.json
  - crim/fixtures/data-2022-fresh/definition.json
  - crim/fixtures/data-2022-fresh/person.json
  - ???
  - definition.json
  - genre
  - person
  - roletype
  - 


9. Start the server with `python3 ./manage.py runserver` (the virtual environment needs to be active).
10. Start a shell with `python3 ./manage.py shell` (the virtual environment needs to be active).
