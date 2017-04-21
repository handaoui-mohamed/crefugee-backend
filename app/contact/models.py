from app import db

class Mail(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	email = db.Column(db.String)
	phone_number = db.Column(db.String)
	body = db.Column(db.String)
	