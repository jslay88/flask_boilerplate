# Flask Boilerplate
This project serves as a structured project boilerplate for Flask driven projects.
This boilerplate utilizes [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), 
[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/), 
[Flask-Login](https://flask-login.readthedocs.io/en/latest/), 
[Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/), 
and [Flask-Script](https://flask-script.readthedocs.io/en/latest/). 
This project is built to be modular, so adapting it to your project should take little to no effort.

**Features**
* Database ORM ([Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/))
* DB Management ([Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/))
* User Login ([Flask-Login](https://flask-login.readthedocs.io/en/latest/))
* API Tokens ([Flask-Login](https://flask-login.readthedocs.io/en/latest/), with custom methods)
* RESTful API ([Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/))
* Modular Structure for Database Models, Front End, and multi-version API backends.
* Starter VueJS and Bootstrap 4 front end template 
(I digress, not the best JS developer, and this should probably be built and served with NodeJS)
* Starter pyTests (Coming Soon)
* Dockerfile Boilerplate

## Getting Started
First, it is advised to clone this project to your dev machine.
Once you have done so, init a new git repository for your project,
and copy the contents of this repository into your new project.

    git clone https://github.com/jslay88/flask_boilerplate.git
    mkdir my_project
    cd my_project
    git init
    cp ../flask_boilerplate/* ./ 

Create a virtual environment in your project, activate it, and install requirements. 
We assume `python` points to Python 3 here.

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Familiarize yourself with the structure of your new project. 
Here are a few key pieces to the structure

* `manage.py` - Script used to handle DB migrations and CLI interaction
* `run.py` - Script used to run the Flask application with logging
* `app/__init__.py` - Application creation and initialization. API version hooks
* `app/config.py` - Application Configuration Definition
* `app/api/v1` - Contains the API Objects, with their Endpoints, Methods, and Serializers
* `app/api/v1/__init__.py` - Hooks for activating API Objects, and other methods/handlers
* `app/database/models.py` - DB Model Definitions
* `app/login/manager.py` - Login manager, methods for handling loading a user/API token
* `app/web/views.py` - Handles the single pane, login, and logout views
* `Dockerfile` - Prebuilt Dockerfile for dockerization of your app
* `docker-compose.yml` - Production type docker-compose file
* `docker-compose.dev.yml` - Local development docker-compose file

Now that you have an idea how this is structured, lets fire it up and make sure it works.
Create the sqlite db, and initialize it using the `manage.py` script, and run the application.

**Local environment without Docker**

    python manage.py -c development db upgrade
    CONFIG=development python run.py
    
**Local environment with Docker**

    docker-compose -f docker-compose.dev.yml up  # Local environment with Docker
    
Access the page at `127.0.0.1:5000`, create a user and test the page out.

## Loose Ends
There is a bit of work to be done on your part to finalize the boilerplate.

### FavIcon
Create a favicon, and use [this site]( https://www.favicon-generator.org/) to generate your favicon set. 
Extract this set into `app/web/site/static/img`

## Database Model Migrations

To build migrations after you have made adjustments to any models within `app.database`

    python manage.py db migrate

To apply those migrations to your test database after verifying the new `.py` in `versions` is correct

    python manage.py db upgrade
    
## Docker and Docker Compose

There is a prebuilt `Dockerfile` and two docker-compose files (`docker-compose.yml` and 
`docker-compose.dev.yml`). `docker-compose.dev.yml` can be used to easily fire up a development 
environment within docker that mounts the local directories for ease of development. Whereas 
`docker-compose.yml` is the standard structure for a production type environment. 

## Project Wish List
* Add Role support (partially there)
* Finish pagination component
* Finish adding `Log` DB events around `APIToken` DB model
* Looking for ideas on what others may need (see below)
* Create pyTest tests

## Contributing
Feel free to fork the repo, make changes, and open pull-requests. I am the first to admit, I 
don't have the best front-end skills. Especially around VueJS (just started). I also built 
this boilerplate in a single sitting in a night. So there might be typos, errors, and other 
things of that sort, but it is tested and working, and was used to kick of another project.

Looking for the following:
* Better ideas on how to hook the front-end (NodeJS?)
* Better ideas around the pagination serializer.
* Better front-end all around. Maybe something more useful out-of-the-box.
* Suggestions, comments, ideas, but trying to avoid it becoming a monolithic project.
* Better role support than what I have planned.
* Replace/Deprecate Flask-Script all together, as Flask has its own CLI tool now 
(haven't had time to figure it out myself).
