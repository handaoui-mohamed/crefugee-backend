# -*- coding: utf-8 -*-
from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from models import Rating
from serializers import rating_model, rating_parser
from app.post.models import Post
from app.user.decorators import login_required

rating_api = api.namespace('ratings', description='Rates for posts by users')

@rating_api.route('')
class Ratings(Resource):
	@rating_api.expect(authorization, rating_model)
	@login_required
	def post(self):
		"""
		Rate a post
		"""
		data = api.payload
		rating_value = data.get("value")
		if rating_value > 5 or rating_value < 0:
			abort(400, {"Value": "la valeur d\'évaluation doit être entre 0 et 5!"})
		post_id = data.get("post_id")
		user_id = g.user.id 
		post = Post.query.get(post_id)
		if not post:
			abort(404)

		rating = Rating.query.filter_by(user_id=user_id, post_id=post.id).first()
		if rating:
			rating.value = rating_value
		else:
			rating = Rating(value=rating_value,user_id=user_id,post_id=post_id)
		db.session.add(rating)
		db.session.commit()

		return {"element": post.to_json()},201

	@rating_api.expect(authorization, rating_parser)
	@login_required
	def get(self):
		"""
		get user's rating for a post
		"""
		post_id = rating_parser.parse_args()['post_id']
		user_id = g.user.id
		rating = Rating.query.filter_by(user_id=user_id, post_id=post_id).first()
		if not rating:
			abort(404)
		return {"element": rating.to_json()}