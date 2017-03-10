from app import db
from app.tag.models import Tag

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
    posted_at = db.Column(db.DateTime)
    helper_post = db.Column(db.Boolean, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": [element.to_json() for element in self.tags],
            "files": [element.to_json() for element in self.files.all()],
            "posted_at": self.posted_at
        }

    def add_tags(self, tags):
        self.tags = []
        for tag_id in tags:
            self.tags.append(Tag.query.get(tag_id))
        return self

    def add_tag(self, tag):
        self.tags.append(tag)
        return self