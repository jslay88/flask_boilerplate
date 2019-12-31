from . import ns as api
from flask_restplus import fields


pagination = api.model('Pagination Options', {
    'page': fields.Integer(description='Page number of current results'),
    'pages': fields.Integer(description='Total number of pages of current results'),
    'per_page': fields.Integer(description='Number of results per page'),
    'total': fields.Integer(description='Total number of results'),
})

serialized_user = api.model('User', {
    'id': fields.Integer(readonly=True, description='User ID'),
    'username': fields.String(required=True, description='Username'),
    'active': fields.Boolean(required=True, description='Active Status'),
    'creation_date': fields.DateTime(readonly=True, description='Account Creation Date')
})

serialized_user_list = api.inherit('User List', pagination, {
    'items': fields.List(fields.Nested(serialized_user))
})

serialized_new_user = api.model('New User', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password (SHA256 Hashed). DO NOT SEND UNHASHED')
})
