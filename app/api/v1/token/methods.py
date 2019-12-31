import logging

from ....database.models import APIToken


logger = logging.getLogger(__name__)


def get_token(token_id, owner_id):
    logger.debug(f'Getting Token ID: {token_id} for Owner ID: {owner_id}')
    rv = APIToken.get(token_id, owner_id, result_required=True)
    logger.debug(f'Received Token: {rv}')
    return rv


def get_tokens(owner_id, page=1, per_page=10):
    logger.debug(f'Retrieving tokens for Owner ID: {owner_id}, Page: {page}, Per Page: {per_page}')
    rv = APIToken.query.filter(APIToken.owner_id == owner_id).paginate(page, per_page)
    logger.debug(f'Retrieved {len(rv.items)} Tokens.')
    return rv


def create_token(owner_id, description):
    logger.debug(f'Creating Token for Owner ID: {owner_id}, Description: {description}')
    rv = APIToken.create(owner_id, description)
    logger.debug(f'Token Created: {rv}')
    return rv


def delete_token(token_id, owner_id):
    logger.debug(f'Deleting Token ID: {token_id}, Owner ID: {owner_id}')
    rv = APIToken.delete(token_id, owner_id)
    logger.debug(f'Token Deleted: {rv}')
    return rv
