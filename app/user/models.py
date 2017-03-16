# -*- coding: utf-8 -*-
from app import db, app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from app.tag.models import Tag
from app.upload.models import ProfilePicture,LegalDocument
from config import SECRET_KEY


UserTag = db.Table(
    'UserTag',
    db.Column('id', db.String, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(60))
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    description = db.Column(db.Text)
    validated = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    refugee = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag', secondary=UserTag, backref='user')
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    files = db.relationship('PostUpload', backref='user', lazy='dynamic')
    profile_image = db.relationship("ProfilePicture", uselist=False, backref="user")
    legal_document = db.relationship("LegalDocument", uselist=False, backref="user")
    sent_messages = db.relationship('Message', backref='sender', lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def to_json(self):
        return {
            'id': self.id,
            'validated': self.validated,
            'is_refugee': self.refugee,
            'username': self.username,
            'full_name': self.full_name,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'description': self.description,
            'tags': [element.to_json() for element in self.tags],
            'profile_image':  self.profile_image.to_json(self.username) if self.profile_image else None
        }

    # for administration
    def to_json_doc(self):
        return {
            'id': self.id,
            'validated': self.validated,
            'is_refugee': self.refugee,
            'username': self.username,
            'full_name': self.full_name,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'description': self.description,
            'tags': [element.to_json() for element in self.tags],
            'legal_document':  self.legal_document.to_json(self.username) if self.legal_document else None
        }

    def to_json_post(self):
        return {
            'id': self.id,
            'validated': self.validated,
            'is_refugee': self.refugee,
            'username': self.username,
            'full_name': self.full_name,
            'address': self.address,
            'email': self.email,
            'phone_number': self.phone_number,
            'description': self.description,
            'tags': [element.to_json() for element in self.tags],
            'posts': [element.to_json() for element in self.posts],
            'profile_image':  self.profile_image.to_json(self.username) if self.profile_image else None
        }


    def add_tags(self, tags):
        self.tags = []
        for tag_id in tags:
            self.tags.append(Tag.query.get(tag_id))
        return self

    def add_tag(self, tag):
        self.tags.append(tag)
        return self

    def __repr__(self):
        return '<User N=%s username=%s location=(%s,%s)>' % (self.id, self.username)
