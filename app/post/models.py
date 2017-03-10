from app import db

PostTag = db.Table(
    'PostTag',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    tags = db.relationship('Tag', secondary=PostTag, backref='post')
    files = db.relationship('PostUpload', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": [element.to_json() for element in self.tags.all()],
            "files": [element.to_json() for element in self.files.all()]
        }