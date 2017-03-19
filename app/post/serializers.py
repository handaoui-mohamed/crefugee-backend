from app import api
from flask_restplus import fields

post_model = api.model('Post', {
    'title': fields.String(required=True),
    'content': fields.String(required=True),
    'tags': fields.List(fields.Integer, description='List containing tags Id', required=True)
})