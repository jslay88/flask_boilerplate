from flask import request
from flask_restplus import Resource
from flask_login import login_required, current_user

from . import ns
from .serializer import serialized_user, serialized_user_list, serialized_new_user
from .methods import get_user, get_users, create_user


@ns.route('')
class UserRoot(Resource):

    @login_required
    @ns.marshal_list_with(serialized_user_list,
                          mask='items{id,username,active},'
                               'page,pages,per_page,total')
    def get(self):
        return get_users(int(request.args.get('page', 1)),
                         int(request.args.get('per_page', 10)))

    @login_required
    @ns.expect(serialized_new_user, validate=True)
    @ns.marshal_with(serialized_user)
    def post(self):
        """
        Creates a new user.

        Make sure the password is SHA256 hashed before sending to API.
        """
        if len(request.json['password']) != 64:
            return 'Password is not SHA256 encoded.', 400
        return create_user(request.json['username'], request.json['password'])


@ns.route('/me')
class CurrentUserItem(Resource):

    @login_required
    @ns.marshal_with(serialized_user,
                     mask='id,username')
    def get(self):
        return current_user


@ns.route('/<int:user_id>')
class UserItem(Resource):

    @login_required
    @ns.marshal_with(serialized_user,
                     mask='id,username,active')
    def get(self, user_id):
        return get_user(user_id)
