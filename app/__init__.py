import logging

from flask import Flask
from flask_migrate import Migrate

from .database import db
from .login import login_manager
from .config import app_config


logger = logging.getLogger(__name__)


def configure_app(flask_app, config_name):
    logger.debug(f'Configuring App with config: {config_name}')
    flask_app.config.from_object(app_config[config_name]())
    flask_app.template_folder = 'web/site/templates'
    flask_app.static_folder = 'web/site/static'


def initialize_app(flask_app):
    logger.debug('Initializing HRS...')
    db.init_app(flask_app)
    login_manager.init_app(flask_app)
    Migrate(flask_app, db)

    from .api.v1 import api_blueprint as api_v1

    from .web.views import web

    logger.debug('Registering Blueprints...')
    flask_app.register_blueprint(api_v1)
    logger.debug('Registered API v1.')
    flask_app.register_blueprint(web)
    logger.debug('Registered Web.')

    if flask_app.config['DEBUG']:
        logger.debug('Application is in DEBUG mode. Setting DEBUG headers.')

        @flask_app.after_request
        def add_header(r):
            """
            Add headers to both force latest IE rendering engine or Chrome Frame,
            and also to disable any cache for the rendered page.
            Should be used sparingly, ergo, development and testing.
            """
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            r.headers["Pragma"] = "no-cache"
            r.headers["Expires"] = "0"
            r.headers['Cache-Control'] = 'public, max-age=0'
            return r


def create_app(config_name='production'):
    logger.debug(f'Creating Application with config: {config_name}')
    app = Flask(__name__)
    configure_app(app, config_name)
    initialize_app(app)
    logger.debug('Application Created!')
    return app
