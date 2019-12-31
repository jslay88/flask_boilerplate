from typing import List
from functools import wraps

from flask import redirect, url_for
from flask_login import LoginManager, current_user

from .models import AnonymousUser
from ..database.models import User, APIToken


login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user is None or not user.active:
        return None
    return user


@login_manager.request_loader
def load_user_from_request(request):
    # X-Api-Key
    api_token = request.headers.get('x-api-key')
    if api_token:
        if APIToken.validate_token(api_token):
            return APIToken.get_owner(api_token, result_required=True)

    # Bearer Token
    api_token = request.headers.get('Authorization')
    if api_token and 'Bearer' in request.headers.get('Authorization')\
            and len(request.headers.get('Authorization').split(' ')) == 2:
        api_token = request.headers.get('Authorization').split(' ')[1]
        if APIToken.validate_token(api_token):
            return APIToken.get_owner(api_token, result_required=True)
    # No header Auth provided
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('web.login'))


def role_required(role: str):
    """
    Wrapper used to check for a single role for current user.

    :param role: String name for the role.
    :type role: str
    :return: The appropriate view based on role status
    """
    def _role_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not current_user.has_role(role):
                return 'Forbidden', 403
            return f(*args, **kwargs)
        return decorated_view
    return _role_required


def roles_required(roles: List[str], require_all: bool = False):
    """
    Wrapper used to check for multiple roles for a current user. User can be required to have all
    roles or only 1 of the provided list.

    :param roles: List of String names for the roles
    :param require_all: If the user is required to have all roles provided in the role list.
    :type roles: list[str]
    :type require_all: bool
    :return: User role status
    :rtype: bool
    """
    def _roles_required(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                raise ValueError('Empty list used when requiring a role.')
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if require_all and not all(current_user.has_role(role) for role in roles):
                return 'Forbidden', 403
            elif not require_all and not any(current_user.has_role(role) for role in roles):
                return 'Forbidden', 403
            return f(*args, **kwargs)
        return decorated_view
    return _roles_required
