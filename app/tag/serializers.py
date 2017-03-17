from app import api
from flask_restplus import fields

tag_model = api.model('Tag', {
    'name': fields.String(required=True)
})