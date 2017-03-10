#!/usr/bin/env python
from app import db, app
import os
from flask import abort, request, jsonify, g, send_from_directory
from werkzeug import secure_filename
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, basedir
from app.upload.models import PostUpload, ProfilePicture, LegalDocument
from app.user.views import login_required


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Route that will process the file upload
@app.route('/api/upload', methods=['POST'])
@login_required
def upload():
    print request.get_data()
    file = request.files.get("file")
    post_id = request.args.get('post_id')
    print post_id
    if post_id:
        post = Post.query.get(post_id)
        if post.user_id is not g.user.id:
            abort(501)
    else:
        abort(404)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        directory = os.path.join(basedir, UPLOAD_FOLDER, 'post', post_id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, filename)
        i = 0
        while os.path.exists(file_path):
            filename = "%s%s"%(i,filename)
            file_path = os.path.join(directory, filename)
        file.save(file_path)
        uploaded_file = PostUpload(name=filename,post=post,user=g.user)
        db.session.add(uploaded_file)
        db.session.commit()
    return jsonify({'element':post.to_json()})


@app.route('/api/uploads/<int:id>', methods=['DELETE'])
@login_required
def delete_file(id):
    file = PostUpload.query.get(id)
    if file and file.user_id == g.user.id:
        db.session.delete(file)
        db.session.commit()
        file_path = os.path.join(basedir, UPLOAD_FOLDER, 'post', file.post_id, file.name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': 'true'}), 200
    abort(404)

@app.route('/api/uploads/post/<int:post_id>/<string:filename>')
def get_file(post_id, filename):
    directory = os.path.join(basedir, UPLOAD_FOLDER, 'post', post_id)
    return send_from_directory(directory, filename)


# profile picture upload
@app.route('/api/upload/profile', methods=['POST'])
@login_required
def upload_profile_image():
    file = request.files.get("profile_image")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        directory = os.path.join(basedir, UPLOAD_FOLDER, g.user.username, 'profile')
        if os.path.exists(directory):
            old_picture = g.user.profile_image_id
            file_path = os.path.join(directory, old_picture.name)
            db.session.delete(old_picture)
            db.session.commit()
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            os.makedirs(directory)
        file_path = os.path.join(directory, filename)
        file.save(file_path)
        uploaded_image = ProfilePicture(name=filename,user=g.user)
        db.session.add(uploaded_image)
        db.session.commit()
        return jsonify({'element':g.user.to_json()})
    abort(400)


@app.route('/api/uploads/profile/<string:username>/<string:filename>')
def get_profile_image(username, filename):
    directory = os.path.join(basedir, UPLOAD_FOLDER, username, 'profile')
    return send_from_directory(directory, filename)


# profile picture upload
@app.route('/api/upload/legaldoucment', methods=['POST'])
@login_required
def upload_legal_document():
    file = request.files.get("legal_document")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        directory = os.path.join(basedir, UPLOAD_FOLDER, g.user.username, 'legal_document')
        if os.path.exists(directory):
            old_document = LegalDocument.query.get(g.user.legal_document_id)
            file_path = os.path.join(directory, old_document.name)
            db.session.delete(old_document)
            db.session.commit()
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            os.makedirs(directory)
        file_path = os.path.join(directory, filename)
        file.save(file_path)
        uploaded_image = LegalDocument(name=filename,user=g.user)
        db.session.add(uploaded_image)
        db.session.commit()
    return jsonify({'element':g.user.to_json()})


@app.route('/api/uploads/legaldocument/<string:username>/<string:filename>')
def get_legal_document(username, filename):
    directory = os.path.join(basedir, UPLOAD_FOLDER, username, 'legal_document')
    return send_from_directory(directory, filename)