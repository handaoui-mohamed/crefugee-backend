from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from app.user.models import User
from app.user.decorators import admin_required
from models import Tag
from serializers import tag_model

tag_api = api.namespace('tags', description='For showing posts and users Tags')

@tag_api.route('')
class Tags(Resource):
    def get(self):
        """
        Returns all tags.
        """
        return {'elements': [element.to_json() for element in Tag.query.all()]}
    
    @tag_api.expect(authorization,tag_model)
    @admin_required
    def post(self):
        """
        Adds a new tag.
        """
        data = api.payload
        name = data.get('name')

        if Tag.query.filter_by(name=name).first() is not None:
            return {'message': "The tag\'s name already exists!"}, 400

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return {'element': tag.to_json()}, 201


@tag_api.route('/<int:id>')
class TagsById(Resource):
    def get(self, id):
        """
        Returns tag by id.
        """
        tag = Tag.query.get(id)
        if tag is None:
            abort(404)
        return {'element': tag.to_json_posts()}

    @tag_api.expect(authorization,tag_model)
    @admin_required
    def put(self, id):
        """
        Update tag's name.
        """
        tag = Tag.query.get(id)
        if tag is None:
            abort(404)

        data = api.payload
        name = data.get('name')

        new_tag = False
        existing_tag = Tag.query.filter_by(name=name).first()
        if (existing_tag is None) or (existing_tag.id == tag.id and not (name == tag.name)): new_tag =True

        if new_tag and name: 
            tag.name = name
            db.session.add(tag)
            db.session.commit()
            return {'element': tag.to_json()}, 201
        return {'message': "The tag\'s name already exists!"}, 400

    @tag_api.expect(authorization)
    @admin_required
    def delete(self, id):
        """
        Delete a tag.
        """
        tag = Tag.query.get(id)
        if tag is None:
            abort(404)
        db.session.delete(tag)
        db.session.commit()
        return '', 204
