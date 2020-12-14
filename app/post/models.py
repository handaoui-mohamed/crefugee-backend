from app import db
from app.tag.models import Tag

PostTag = db.Table(
    'PostTag',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('post_id', db.String, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String)
    tags = db.relationship('Tag', secondary=PostTag, backref='post')
    image = db.relationship('PostUpload', uselist=False, backref='post')
    user_id = db.Column(db.String, db.ForeignKey("user.id"))
    posted_at = db.Column(db.DateTime)
    refugee_post = db.Column(db.Boolean, default=False)
    ratings = db.relationship('PostRating', backref='post', lazy='dynamic')

    def to_json(self):
        from app.user.models import User
        post_rating = 0
        len_ratings = len(self.ratings.all())
        if  len_ratings > 0:
            for rating in self.ratings.all():
                post_rating += rating.value
            post_rating = post_rating / len_ratings
        
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": [element.to_json() for element in self.tags],
            "image": self.image.to_json() if self.image else None,
            "user": User.query.get(self.user_id).to_json(),
            "posted_at": str(self.posted_at),
            "refugee_post": self.refugee_post,
            "rating": post_rating
        }

    def add_tags(self, tags):
        self.tags = []
        for tag_id in tags:
            self.tags.append(Tag.query.get(tag_id))
        return self

    def add_tag(self, tag):
        self.tags.append(tag)
        return self
