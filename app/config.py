import os


class Config(object):
    """
    Parent configuration class.
    """
    CONFIG_NAME = 'BaseConfig'
    DEBUG = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 230
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{DB_USER}:{DB_PASS}@' \
                              '{DB_HOST}:{DB_PORT}/{DB_NAME}' \
        .format(DB_USER=os.getenv('DB_USER', 'postgres'),
                DB_PASS=os.getenv('DB_PASS', 'postgres'),
                DB_HOST=os.getenv('DB_HOST', 'postgres'),
                DB_PORT=os.getenv('DB_PORT', 5432),
                DB_NAME=os.getenv('DB_NAME', 'postgres'))


class DevelopmentConfig(Config):
    """
    Configurations for Development.
    """
    CONFIG_NAME = 'development'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = 'DEVELOPMENT'

    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.db")}'


class TestingConfig(Config):
    """
    Configurations for Testing, with a separate test database.
    """
    CONFIG_NAME = 'testing'
    TESTING = True
    DEBUG = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.path.dirname(os.path.realpath(__file__)), "db.db")}'
    # LOGIN_DISABLED = True


class StagingConfig(Config):
    """
    Configurations for Staging.
    """
    CONFIG_NAME = 'staging'
    DEBUG = True


class ProductionConfig(Config):
    """
    Configurations for Production.
    """
    CONFIG_NAME = 'production'
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
