import os
import sys
import logging

from app import create_app, app_config


logger = logging.getLogger()
handler = logging.StreamHandler(stream=sys.stdout)
handler.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s: %(message)s')
logger.addHandler(handler)
logger.setLevel(app_config[os.getenv('CONFIG', 'production')].LOG_LEVEL)
logger.propagate = True

app = create_app(os.getenv('CONFIG', 'production'))


if __name__ == '__main__':
    app.run()
