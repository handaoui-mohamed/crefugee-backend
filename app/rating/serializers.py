from app import api
from flask_restplus import fields, reqparse

rating_model = api.model('Rating', {
    'value': fields.Float(required=True, max=5),
    'post_id': fields.String(required=True)
})

# Request Parsers
rating_parser = reqparse.RequestParser()
rating_parser.add_argument('post_id', type=str, help='Post id is required', required=True)