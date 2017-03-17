# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length
from app.user.models import User
from app import api
from flask_restplus import fields

class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[
        DataRequired('Le nom d\'utilisateur est nécessaire'),
        Length(min=1, max=32, message="Le nom d\'utilisateur doit être > 1 et < 32 caractères")
    ])
    email = EmailField('email', [
        validators.DataRequired('L\'addresse Email est nécessaire'),
        validators.Email('L\'addresse Email doit être valide')
    ])
    password = PasswordField('password', validators=[
        Length(min=8, message="Le nom mot de passe doit être > 8 caractères"),
        DataRequired('Le mot de passe est nécessaire')
    ])


    def validate(self):
        if not FlaskForm.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            self.username.errors.append("Ce nom d'utilisteur existe déja, veuillez choisir un autre!")
            return False
        return True


class UpdateForm(FlaskForm):
    address = StringField('address', validators=[
        Length(max=200, message="L\'addresse doit être < 200 caractères")
    ])
    full_name = StringField('full_name', validators=[
        Length(max=100, message="Le nom et prénom doivent être < 100 caractères")
    ])
    phone_number = StringField('phone_number', validators=[
        Length(max=20, message="Le numéro téléphone doit être < 20 numéro")
    ])
    description = StringField('description', validators=[
        Length(max=10000, message="La description doit être < 10000 caractères")
    ])


class AdminLoginForm(FlaskForm):
    username = StringField('username',validators=[
        DataRequired('Le nom d\'utilisateur est nécessaire'),
        Length(min=1, max=32, message="Le nom d\'utilisateur doit être > 1 et < 32 caractères")
    ])
    password = PasswordField('password', validators=[
        Length(min=8, message="Le nom mot de passe doit être > 8 caractères"),
        DataRequired('Le mot de passe est nécessaire')
    ])
    remember_me = BooleanField('remember_me', default=False)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        
        user = User.query.filter_by(username=self.username.data).first()
        if not user or not user.verify_password(self.password.data) or not user.is_moderator:
            return False
        return True

# Models for swagger
registration_model = api.model('User', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'is_refugee': fields.Boolean
})