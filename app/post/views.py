from app import app, db
from flask import abort, request, jsonify, g
from werkzeug.datastructures import MultiDict
from app.tag.models import Tag
from app.post.models import Post
from app.post.forms import PostForm
from app.user.views import login_required
from datetime import datetime
from config import POSTS_PER_PAGE

@app.route('/api/post', methods=['POST'])
@login_required
def new_post():
    data = request.get_json(force=True)
    tags = data.get('tags')
    if not tags:
        abort(400)
    form = PostForm(MultiDict(mapping=data))
    if form.validate():
        title = data.get('title')
        content = data.get('content')
        helper_post = data.get('helper_post', False)
        post = Post(title=title.lower(), content=content, user=g.user, posted_at=datetime.utcnow(), helper_post=helper_post)
        post.add_tags(tags)
        db.session.add(post)
        db.session.commit()
        return jsonify({'element': post.to_json()})
    return jsonify({"form_errors": form.errors}), 400

@app.route('/api/post/<int:post_id>', methods=['PUT'])
@login_required
def modify_post(post_id):
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
        return jsonify({'element': post.to_json()})
    return jsonify({"form_errors": form.errors}), 400

@app.route('/api/post/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return jsonify({'element':post.to_json()})

@app.route('/api/post/<int:post_id>', methods=["DELETE"])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post or post.user_id is not g.user.id:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'sucess':'true'})

@app.route('/api/post/helper')
@app.route('/api/post/helper/<int:page>')
def get_helper_post(page=1):
    posts = Post.query.filter_by(helper_post=True).order_by(Post.posted_at.desc()).paginate(page, POSTS_PER_PAGE, False).items
    return jsonify({'elements': [element.to_json() for element in posts]})

@app.route('/api/post/refugee')
@app.route('/api/post/refugee/<int:page>')
def get_refugee_post(page=1):
    posts = Post.query.filter_by(helper_post=False).order_by(Post.posted_at.desc()).paginate(page, POSTS_PER_PAGE, False).items
    return jsonify({'elements': [element.to_json() for element in posts]})