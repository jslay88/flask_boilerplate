from flask import request
from flask_restx import Resource
from flask_login import login_required, current_user

from . import ns
from .serializer import serialized_token, serialized_token_list, \
    serialized_new_token, serialized_token_with_token
from .methods import get_token, get_tokens, create_token, delete_token


@ns.route('')
class TokenRoot(Resource):

    @login_required
    @ns.marshal_list_with(serialized_token_list,
                          mask='items{id,description,active},'
                               'page,pages,per_page,total')
    def get(self):
        return get_tokens(current_user.id,
                          int(request.args.get('page', 1)),
                          int(request.args.get('per_page', 10)))

    @login_required
    @ns.expect(serialized_new_token, validate=True)
    @ns.marshal_with(serialized_token_with_token)
    def post(self):
        """
        Creates a new token.

        Description should be something meaningful to identify the token by.
        You will only get to see the token on the response for create.
        """
        description = request.json['description']
        return create_token(current_user.id, description)


@ns.route('/<int:token_id>')
class TokenItem(Resource):

    @login_required
    def delete(self, token_id):
        if delete_token(token_id, current_user.id):
            return '', 200
        return 'Token Not Found', 404
