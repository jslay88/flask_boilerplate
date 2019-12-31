from . import ns as api
from flask_restplus import fields


pagination = api.model('Pagination Options', {
    'page': fields.Integer(description='Page number of current results'),
    'pages': fields.Integer(description='Total number of pages of current results'),
    'per_page': fields.Integer(description='Number of results per page'),
    'total': fields.Integer(description='Total number of results'),
})

serialized_token = api.model('Token', {
    'id': fields.Integer(description='Token ID'),
    'description': fields.String(required=True, description='Meaningful Description'),
    'active': fields.Boolean(description='Active state')
})

serialized_token_with_token = api.model('Token Private', {
    'id': fields.Integer(description='Token ID'),
    'token': fields.String(description='Newly Created API Token. Store this, as you will '
                                       'only receive it on creation.')
})

serialized_token_list = api.inherit('Token List', pagination, {
    'items': fields.List(fields.Nested(serialized_token))
})

serialized_new_token = api.model('New Token', {
    'description': fields.String(required=True, description='Meaningful Description'),
})
