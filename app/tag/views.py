from app import db, api
from flask_restplus import Resource
from flask import abort, request, g
from app.user.models import User
from app.tag.models import Tag

# add auth required and verify admin role

tag_api = api.namespace('tags', description='For showing posts and users Tags')

# new tag
@tag_api.route('')
class Tags(Resource):
    def get(self):
        return {'elements': [element.to_json() for element in Tag.query.all()]}
    
    def post(self):
        data = request.get_json(force=True)
        name = data.get('name')
        pass_code = data.get('pass_code')

        if pass_code is None or name is None or Tag.query.filter_by(name=name).first() is not None:
            abort(400)    # missing arguments or existing one 

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return {'element': tag.to_json()}, 201


@tag_api.route('/<int:id>')
class TagsById(Resource):
    def get(self, id):
        tag = Tag.query.get(id)
        if tag is None:
            abort(400)
        return {'element': tag.to_json_users()}

    def put(self, id):
        tag = Tag.query.get(id)
        if tag is None:
            abort(400)
        data = request.get_json(force=True)
        name = data.get('name')
        description = data.get('description', tag.description)
        pass_code = data.get('pass_code')

        if pass_code is None:
            abort(400)

        new_tag = False
        existing_tag = Tag.query.filter_by(name=name).first()
        if (existing_tag is None) or (existing_tag.id == tag.id and not (name == tag.name)): new_tag =True

        if new_tag and name: tag.name = name
        db.session.add(tag)
        db.session.commit()
        return {'element': tag.to_json()}, 201

    def delete(self, id):
        tag = Tag.query.get(id)
        db.session.delete(tag)
        db.session.commit()
        return '', 204
