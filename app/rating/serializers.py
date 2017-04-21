from app import api
from flask_restplus import fields, reqparse

post_rating_model = api.model('Rating', {
    'value': fields.Float(required=True, max=5),
    'post_id': fields.String(required=True)
})

# Request Parsers
post_rating_parser = reqparse.RequestParser()
post_rating_parser.add_argument('post_id', type=str, help='Post id is required', required=True)

user_rating_model = api.model('Rating', {
    'value': fields.Float(required=True, max=5),
    'rated_user_id': fields.String(required=True)
})

# Request Parsers
user_rating_parser = reqparse.RequestParser()
user_rating_parser.add_argument('rated_user_id', type=str, help='Rated user id is required', required=True)