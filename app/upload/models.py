from app import db
from config import HOST_URL, UPLOAD_FOLDER

# file upload
class PostUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    post_id = db.Column(db.String, db.ForeignKey('post.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

    def to_json(self):
        return {
            'id': self.id,
            'path': HOST_URL+'/posts/'+UPLOAD_FOLDER+"/"+self.post_id+"?filename="+self.name,
            'name': self.name
        }


# file upload
class ProfilePicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

    def to_json(self, username):
        return {
            'id': self.id,
            'path': HOST_URL+'/profile/'+UPLOAD_FOLDER+"?username="+username+"&filename="+self.name,
            'name': self.name,
            'user_id': self.user_id
        }

# file upload
class LegalDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

    def to_json(self, username):
        return {
            'id': self.id,
            'path': HOST_URL+'/legaldocument/'+UPLOAD_FOLDER+"?username="+username+"&filename="+self.name,
            'name': self.name,
            'user_id': self.user_id
        }