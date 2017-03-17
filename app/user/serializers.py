from app import api
from flask_restplus import fields

# Models for swagger
registration_model = api.model('User registration', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_refugee': fields.Boolean
})

user_login_model = api.model('User login model', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'remember_me': fields.Boolean
})

profile_model = api.model('User profile', {
    'full_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'description': fields.String,
    'address': fields.String,
    'phone_number': fields.String,
    'tags': fields.List(fields.Integer, description='List containing tags Id')
})