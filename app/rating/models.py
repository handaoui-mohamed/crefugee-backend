from app import db

class Rating(db.Model):
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
