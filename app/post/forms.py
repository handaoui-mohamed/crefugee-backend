# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField,FieldList
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('title',validators=[
        DataRequired('Le titre de la publication est nécessaire'),
        Length(min=5, max=32, message="Le titre doit être > 5 et < 100 caractères")
    ])
    content = StringField('content',validators=[
        DataRequired('Le contenu de la publication est nécessaire')
    ])