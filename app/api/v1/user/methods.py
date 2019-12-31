import logging

from ....database.models import User


logger = logging.getLogger(__name__)


def get_user(user_id):
    logger.debug(f'Getting User ID: {user_id}')
    rv = User.get(User.id == user_id, result_required=True)
    logger.debug(f'Received User: {rv}')
    return rv


def get_users(page=1, per_page=10):
    logger.debug(f'Get User Page. Page: {page}, Per Page: {per_page}')
    rv = User.query.paginate(page, per_page)
    logger.debug(f'Retrieved {len(rv.items)} Users.')
    return rv


def create_user(username, password):
    logger.debug(f'Create User. Username: {username}, Password: {"*" * len(password)}')
    rv = User.create(username, password)
    logger.debug(f'Created User: {rv}')
    return rv
