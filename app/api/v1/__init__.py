from flask import Blueprint
from flask_restx import Api, apidoc
from flask_login import login_required

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

# Namespace import
from .user.endpoints import ns as user_namespace
from .token.endpoints import ns as token_namespace
from .log.endpoints import ns as log_namespace


api_blueprint = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_blueprint, title='Flask Boilerplate API', version='1.0.0')

api.add_namespace(user_namespace)
api.add_namespace(token_namespace)
api.add_namespace(log_namespace)


@api.errorhandler(NoResultFound)
def handle_no_result_exception(error):
    """
    Return a custom not found error message and 404 status code
    """
    return {'message': str(error)}, 404


@api.errorhandler(IntegrityError)
def handle_integrity_error(error):
    """
    Likely a Key Restraint Error.
    """
    return {'message': str(error)}, 400


@api.documentation
@login_required
def swagger_ui():
    """
    API Docs are only available for logged in users.
    :return:
    """
    return apidoc.ui_for(api)
