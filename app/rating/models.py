from app import db

class PostRating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Float)
	post_id = db.Column(db.String, db.ForeignKey('post.id'))
	user_id = db.Column(db.String, db.ForeignKey('user.id'))


	def to_json(self):
		return{
			"id": self.id,
			"value": self.value,
			"post_id": self.post_id,
			"user_id": self.user_id
		}

class UserRating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	value = db.Column(db.Float)
	user_id = db.Column(db.String)
	rated_user_id = db.Column(db.String, db.ForeignKey('user.id'))


	def to_json(self):
		return{
			"id": self.id,
			"value": self.value,
			"user_id": self.user_id,
			"rated_user_id": self.rated_user_id
		}
