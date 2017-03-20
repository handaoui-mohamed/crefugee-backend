from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from app.tag.models import Tag
from models import Post
from forms import PostForm
from serializers import post_model
from app.user.decorators import login_required
from datetime import datetime
from config import POSTS_PER_PAGE
import uuid

post_api = api.namespace('posts', description='For sending and showing users posts')

@post_api.route('')
class NewPost(Resource):
    @post_api.expect(authorization, post_model)
    @login_required
    def post(self):
        """
        Adds a new post
        """
        data = api.payload
        tags = data.get('tags')
        if not tags:
            abort(400)
        form = PostForm.from_json(data)
        if form.validate():
            title = data.get('title')
            content = data.get('content')
            post = Post(id=uuid.uuid4().hex,title=title.lower(), content=content, user=g.user,\
                        posted_at=datetime.utcnow(), refugee_post=g.user.refugee)
            post.add_tags(tags)
            db.session.add(post)
            db.session.commit()
            return {'element': post.to_json()}, 201
        return {"form_errors": form.errors}, 400

    def get(self):
        """
        Returns all post
        """
        posts = Post.query.all()
        return {'elements': [element.to_json() for element in posts]}

@post_api.route('/<int:post_id>')
class PostById(Resource):
    @post_api.expect(authorization, post_model)
    @login_required
    def put(self, post_id):
        """
        Updates a post
        """
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        data = api.payload
        tags = data.get('tags',post.tags)
        if not tags:
            abort(400)
        form = PostForm.from_json(data)
        if form.validate():
            post.title = data.get('title')
            post.content = data.get('content')
            post.add_tags(tags)
            post.posted_at = datetime.utcnow()
            db.session.add(post)
            db.session.commit()
            return {'element': post.to_json()}, 201
        return {"form_errors": form.errors}, 400

    def get(self, post_id):
        """
        Returns a post by id
        """
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        return {'element':post.to_json()}

    @post_api.expect(authorization)
    @login_required
    def delete(self, post_id):
        """
        Deletes a post
        """
        post = Post.query.get(post_id)
        if not post or post.user_id is not g.user.id:
            abort(404)
        db.session.delete(post)
        db.session.commit()
        return '', 204

@post_api.route('/helper','/helper/<int:page>')
class HelperPost(Resource):
    def get(self, page=1):
        """
        Returns all helpers posts
        """
        posts = Post.query.filter_by(refugee_post=False).order_by(Post.posted_at.desc()).paginate(page, POSTS_PER_PAGE, False).items
        return {'elements': [element.to_json() for element in posts]}

@post_api.route('/refugee','/refugee/<int:page>')
class RefugeePost(Resource):
    def get(self, page=1):
        """
        Returns all refugees posts
        """
        posts = Post.query.filter_by(refugee_post=True).order_by(Post.posted_at.desc()).paginate(page, POSTS_PER_PAGE, False).items
        return {'elements': [element.to_json() for element in posts]}