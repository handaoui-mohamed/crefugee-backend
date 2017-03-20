import jwt
from jwt import DecodeError, ExpiredSignature
from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, g
from config import SECRET_KEY
from models import User


# JWT AUTh process start
def create_token(user, days=1):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=days)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']
        g.user = User.query.get(g.user_id)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not g.user.is_administrator:
            response = jsonify(message='User do not have the right permission')
            response.status_code = 403
            return response
        return f(*args, **kwargs)
    return decorated_function


def moderator_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not g.user.is_moderator:
            response = jsonify(message='User do not have the right permission')
            response.status_code = 403
            return response
        return f(*args, **kwargs)
    return decorated_function