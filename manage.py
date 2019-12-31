import os
import sys
import hashlib
import logging

from flask_script import Manager
from flask_migrate import MigrateCommand

from app import create_app, app_config
from app.database.models import User


logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stdout)
handler.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s: %(message)s')
logger.addHandler(handler)
logger.setLevel(app_config[os.getenv('CONFIG', 'production')].LOG_LEVEL)
logger.propagate = True


manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config_name', required=False, default='production')
manager.add_command('db', MigrateCommand)


@manager.command
@manager.option('-u', '--username', dest='username', required=True)
@manager.option('-p', '--password', dest='password', required=True)
@manager.option('-a', '--active', dest='active', default=True)
def create_user(username, password, active=True):
    with manager.app.app_context():
        User.create(username,
                    str(hashlib.sha256(password.encode('utf-8')).hexdigest()),
                    active)
    print('User created!')


if __name__ == '__main__':
    manager.run()
