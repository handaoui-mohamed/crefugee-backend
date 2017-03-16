from app import db, api
from flask_restplus import Resource
from app.user.models import User
from app.user.auth import create_token, parse_token, login_required
from app.user.forms import RegistrationForm, UpdateForm
from app.tag.models import Tag
from flask import abort, request, g
from config import YEAR, DAY, SECRET_KEY
from werkzeug.datastructures import MultiDict
import uuid

users_api = api.namespace('users', description='All operations about USERS')

@users_api.route('')
class Users(Resource):
    def post(self):
        data = request.get_json(force=True)
        form = RegistrationForm(MultiDict(mapping=data))
        if form.validate():
            username = data.get('username')
            password = data.get('password')
            helper = data.get('is_refugee', False)
            email = data.get('email')
            remember_me = data.get('remember_me', False)
            user = User(id=uuid.uuid4().hex,username=username.lower(), email=email.lower(), refugee=refugee)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            duration = DAY if not remember_me else YEAR
            token = create_token(user, duration)
            return {'token': token.decode('ascii'), 'user_id': user.id}, 201
        return {"form_errors": form.errors}, 400

    def get(self):
        users = User.query.all()
        return  {'elements': [element.to_json() for element in users]}


@users_api.route('/<string:id>')
class UserById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404)
        return {'element':user.to_json()}

@users_api.route('/username/<string:username>')
class UserByUsername(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        return {'element':user.to_json_post()}

users_login = api.namespace('login', description='User login')
@users_login.route('')
class Login(Resource):
    def post(self):
        data = request.get_json(force=True)
        username = data.get('username')
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
    @login_required
    def get(self):
        return {'element':g.user.to_json()}
        
    @login_required
    def put(self):
        user = g.user
        data = request.get_json(force=True)
        form = UpdateForm(MultiDict(mapping=data))
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
        return {"form_errors": form.errors}, 400