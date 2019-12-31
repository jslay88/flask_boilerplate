import logging
from uuid import uuid4

from flask_login import UserMixin
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


logger = logging.getLogger(__name__)


class ColumnCreationDate(object):
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)


class User(db.Model, ColumnCreationDate, UserMixin):
    logger = logging.getLogger(__name__ + '.User')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.VARCHAR(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(self, username, password, active=True):
        self.username = username
        self.password = password
        self.active = active

    def set_password(self, password):
        self.logger.debug(f'Setting Password for User ID: {self.id}')
        self.password = generate_password_hash(password)
        self.logger.debug(f'Password set for User ID: {self.id}')
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def create(cls, username, password, active=True):
        cls.logger.debug('Creating New User')
        rv = User(username, generate_password_hash(password), active)
        db.session.add(rv)
        db.session.commit()
        db.session.flush()
        cls.logger.debug(f'New user created with ID: {rv.id}.')
        Log.create('New User {associated_user.username} Created!', rv.id)
        return rv

    @classmethod
    def get(cls, user_id, result_required=False):
        cls.logger.debug(f'Getting User ID: {user_id}')
        rv = User.query.filter(User.id == user_id).first()
        if result_required and rv is None:
            cls.logger.warning(f'Found no User when one was required. User ID: {user_id}')
            raise NoResultFound(f'A User database result was required and none was found. '
                                f'User ID: {user_id}')
        cls.logger.debug(f'Received User: {rv}')
        return rv

    @classmethod
    def authenticate(cls, username, password):
        cls.logger.debug(f'Authentication Request for {username}.')
        user = User.query.filter(User.username == username).first()
        if user is None or not user.active:
            cls.logger.debug(f'User {username} does not exist or is not active.')
            return False
        auth_status = user.check_password(password)
        cls.logger.debug(f'Authentication Results: {"PASS" if auth_status else "FAIL"}')
        if not auth_status:
            Log.create('{associated_user.username} failed login attempt.', user.id)
        return user.check_password(password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def has_role(_):
        """
        Future Role implementations
        """
        return True


class APIToken(db.Model, ColumnCreationDate):
    logger = logging.getLogger(__name__ + '.APIToken')

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.VARCHAR(32), unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.VARCHAR(128), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    owner = db.relationship('User', backref=db.backref('api_tokens', lazy='dynamic'), lazy='joined')

    def __init__(self, token, owner_id, description=None, active=True):
        self.token = token
        self.owner_id = owner_id
        self.description = description
        self.active = active

    def __repr__(self):
        return f'<APIToken: {self.id}>'

    @classmethod
    def create(cls, owner_id, description=None):
        cls.logger.info(f'Creating New API Token for User ID: {owner_id}')
        rv = APIToken(str(uuid4()).replace('-', ''), owner_id, description)
        db.session.add(rv)
        db.session.commit()
        cls.logger.info(f'API Token Created for User ID: {owner_id}')
        return rv

    @classmethod
    def get(cls, token_id, owner_id, result_required=False):
        cls.logger.debug(f'Getting Token ID: {token_id}, Owner ID: {owner_id}'
                         f'Result Required: {result_required}')
        rv = APIToken.query.filter(APIToken.id == token_id,
                                   APIToken.owner_id == owner_id).first()
        if result_required and rv is None:
            cls.logger.warning(f'Found no API Token when one was required. Token ID: {token_id}, Owner ID: {owner_id}')
            raise NoResultFound(f'An API Token database result was required and none was found. '
                                f'Token ID: {token_id}, Owner ID: {owner_id}')
        cls.logger.debug(f'Received Token: {rv}')
        return rv

    @classmethod
    def get_owner(cls, token, result_required=False):
        cls.logger.debug(f'Getting Owner for Token (last 4): {token[-4:]}')
        rv = APIToken.query.filter(APIToken.token == token).first()
        if result_required and rv is None:
            cls.logger.warning(f'Found no API Token when one was required. Token (last 4): {token[-4:]}')
            raise NoResultFound(f'An API Token database result was required and none was found. '
                                f'Token (last 4): {token[-4:]}')
        cls.logger.debug(f'Received Token: {token}. Owner: {token.owner}')
        return rv.owner

    @classmethod
    def delete(cls, token_id, owner_id):
        cls.logger.debug(f'Deleting (deactivating) API Token ID: {token_id}, User ID: {owner_id}')
        token = APIToken.query.filter(APIToken.id == token_id,
                                      APIToken.owner_id == owner_id).first()
        cls.logger.debug(f'Received Token: {token}')
        if token is None:
            cls.logger.warning(f'Attempt to delete token where either the token didn\'t exist,'
                               f'or the user associated doesn\'t own the token. '
                               f'Attempted Token ID: {token_id}, Attempted Owner ID: {owner_id}')
            return False
        token.deactivate()
        cls.logger.debug(f'API Token Deleted (deactivated). Token ID: {token.id}')
        return True

    @property
    def is_valid(self):
        if not self.owner.active or not self.active:
            return False
        return True

    @classmethod
    def validate_token(cls, token):
        cls.logger.debug(f'Validating Token (last 4): {token[-4:]}')
        token = APIToken.query.filter(APIToken.token == token).first()
        if token is None or not token.is_valid:
            cls.logger.debug(f'Invalid Token (last 4): {token[-4:]}')
            return False
        cls.logger.debug(f'Valid Token (last 4): {token[-4:]}')
        return True

    def deactivate(self):
        self.active = False
        db.session.commit()


class Log(db.Model, ColumnCreationDate):
    logger = logging.getLogger(__name__ + '.Log')

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    associated_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    associated_user = db.relationship(User, backref=db.backref('logs', lazy='dynamic'), lazy='joined')

    def __init__(self, message, associated_user_id):
        self.message = message
        self.associated_user_id = associated_user_id

    @classmethod
    def create(cls, message, associated_user_id):
        cls.logger.debug(f'Creating Log: User ID: {associated_user_id}, Message: {message}')
        rv = Log(message, associated_user_id)
        db.session.add(rv)
        db.session.commit()
        db.session.flush()
        cls.logger.debug(f'Log created, ID: {rv.id}')
        return rv

    @classmethod
    def get(cls, log_id, result_required=False):
        cls.logger.debug(f'Getting Log ID: {log_id}')
        rv = Log.query.filter(Log.id == log_id).first()
        if result_required and rv is None:
            cls.logger.warning(f'Found no Log when one was required. Log ID: {log_id}')
            raise NoResultFound(f'A log database result was required and none was found. '
                                f'Log ID: {log_id}')
        cls.logger.debug(f'Received Log: {rv}')
        return rv

    @property
    def formatted(self):
        return self.message.format(**self.__dict__)
