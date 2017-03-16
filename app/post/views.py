from app import db, api
from flask_restplus import Resource
from flask import abort, request, g
from werkzeug.datastructures import MultiDict
from app.tag.models import Tag
from app.post.models import Post
from app.post.forms import PostForm
from app.user.auth import login_required
from datetime import datetime
from config import POSTS_PER_PAGE

post_api = api.namespace('Posts', description='For sending and showing users posts')

@post_api.route('/posts', endpoint="Add a post")
class NewPost(Resource):
    @login_required
    def post(self):
        data = request.get_json(force=True)
        tags = data.get('tags')
        if not tags:
            abort(400)
        form = PostForm(MultiDict(mapping=data))
        if form.validate():
            title = data.get('title')
            content = data.get('content')
            helper_post = data.get('helper_post', False)
            post = Post(title=title.lower(), content=content, user=g.user,\
                        posted_at=datetime.utcnow(), helper_post=helper_post)
            post.add_tags(tags)
            db.session.add(post)
            db.session.commit()
            return {'element': post.to_json()}, 201
        return {"form_errors": form.errors}, 400

    def get(self):
        posts = Post.query.all()
        return {'elements': [element.to_json() for element in posts]}

@post_api.route('/posts/<int:post_id>')
class PostById(Resource):
    @login_required
    def put(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        data = request.get_json(force=True)
        tags = data.get('tags',post.tags)
        if not tags:
            abort(400)
        form = PostForm(MultiDict(mapping=data))
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
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        return {'element':post.to_json()}

    @login_required
    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post or post.user_id is not g.user.id:
            abort(404)
        db.session.delete(post)
        db.session.commit()
        return '', 204

@post_api.route('/posts/helper')
@post_api.route('/post/helper/<int:page>')
class HelperPost(Resource):
    def get(self, page=1):
        posts = Post.query.filter_by(helper_post=True).order_by(Post.posted_at.desc()).paginate(page, POSTS_PER_PAGE, False).items
        return {'elements': [element.to_json() for element in posts]}

@post_api.route('/posts/refugee')
@post_api.route('/posts/refugee/<int:page>')
class RefugeePost(Resource):
    def get(self, page=1):
        posts = Post.query.filter_by(helper_post=False).order_by(Post.posted_at.desc()).paginate(page, POSTS_PER_PAGE, False).items
        return {'elements': [element.to_json() for element in posts]}