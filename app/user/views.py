from app import db, api, authorization
from flask_restplus import Resource
from models import User
from decorators import create_token, parse_token, login_required, admin_required
from serializers import registration_model, user_login_model, profile_model, users_parser
from forms import RegistrationForm, UpdateForm
from app.tag.models import Tag
from flask import abort, g
from config import YEAR, DAY
import uuid

users_api = api.namespace('users', description='All operations about USERS')

@users_api.route('')
class Users(Resource):
    @users_api.expect(registration_model)
    def post(self):
        """
        Adds a new User.
        """
        data = api.payload
        form = RegistrationForm.from_json(data)
        if form.validate():
            username = data.get('username')
            password = data.get('password')
            refugee = data.get('is_refugee', False)
            email = data.get('email')
            user = User(id=uuid.uuid4().hex,username=username.lower(), email=email.lower(), refugee=refugee, role_id=1)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return {'element': user.to_json()}, 201
        return {"message": form.errors}, 400

    @users_api.expect(users_parser)
    def get(self):
        """
        Returns all users.
        """
        username = users_parser.parse_args()['username']
        if not username: 
            return {'elements': [element.to_json() for element in User.query.all()]}
        user = User.query.filter_by(username=username).first()
        if not user: abort(404)
        return  {'element': user.to_json_post()}


@users_api.route('/<string:id>')
@users_api.response(404, 'User not found')
@users_api.response(200, 'User profile without posts')
@users_api.param('id', 'The user\'s id')
class UserById(Resource):
    @users_api.expect(authorization)
    @login_required
    def get(self, id):
        """
        Returns a user by id.
        """
        user = User.query.get(id)
        if not user:
            abort(404)
        return {'element':user.to_json()}

users_login = api.namespace('login', description='User login')

@users_login.route('')
class Login(Resource):
    @users_login.expect(user_login_model)
    def post(self):
        """
        Used to login a user, returns Token and User.
        """
        data = api.payload
        username = data.get('username').lower()
        password = data.get('password')
        remember_me = data.get('remember_me', False)
        duration = DAY if not remember_me else YEAR
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            abort(404)
        g.user = user
        token = create_token(g.user, duration)
        return {'token': token.decode('ascii'), 'user': g.user.to_json()}


users_profile = api.namespace('profile', description='User profile')
@users_profile.route('')
class Profile(Resource):
    
    @users_api.expect(authorization)
    @login_required
    def get(self):
        """
        Returns current user's profile.
        """
        return {'element':g.user.to_json()}
        
    @users_profile.expect(authorization,profile_model)
    @login_required
    def put(self): 
        """
        Update current user's profile.
        """
        user = g.user
        data = api.payload
        form = UpdateForm.from_json(data)
        if form.validate():
            password = data.get('password')
            full_name = data.get('full_name', user.full_name)
            address = data.get('address', user.address)
            email = data.get('email', user.email)
            phone_number = data.get('phone_number', user.phone_number)
            description = data.get('description', user.description)
            tags = data.get('tags', user.tags)

            if data.get('tags') is not None: user.add_tags(tags)

            if full_name:user.full_name=full_name.lower()
            if address: user.address=address.lower()
            user.email=email.lower()
            user.phone_number=phone_number
            user.description=description
            if password: user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return {'element':user.to_json()}, 201
        return {"message": form.errors}, 400