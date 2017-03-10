import os
from app import db, app
from config import HOST_URL, UPLOAD_FOLDER

# file upload
class PostUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        return {
            'id': self.id,
            'path': os.path.join(HOST_URL, UPLOAD_FOLDER, 'post', post_id).replace("\\", "/"),
            'name': self.name
        }


# file upload
class ProfilePicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self, username):
        return {
            'id': self.id,
            'path': os.path.join(HOST_URL, UPLOAD_FOLDER, 'profile', username, self.name).replace("\\", "/"),
            'name': self.name,
            'user_id': self.user_id
        }

# file upload
class LegalDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self, username):
        return {
            'id': self.id,
            'path': os.path.join(HOST_URL, UPLOAD_FOLDER, 'legal_document', username, self.name).replace("\\", "/"),
            'name': self.name,
            'user_id': self.user_id
        }