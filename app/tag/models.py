from app import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    users = db.relationship('User', secondary='UserTag', backref='tag')
    posts = db.relationship('Post', secondary='PostTag', backref='tag')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'nb_users': len(self.users),
            'nb_post': len(self.posts)
        }

    def to_json_users(self):
        return {
            'id': self.id,
            'name': self.name,
            'nb_users': len(self.users),
            'users': [element.to_json() for element in self.users]
        }

    def to_json_posts(self):
        return {
            'id': self.id,
            'name': self.name,
            'nb_post': len(self.posts),
            'posts': [element.to_json() for element in self.posts]
        }
