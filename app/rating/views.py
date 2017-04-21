# -*- coding: utf-8 -*-
from app import db, api, authorization
from flask_restplus import Resource
from flask import abort, g
from models import PostRating, UserRating
from serializers import post_rating_model, post_rating_parser, user_rating_model, user_rating_parser
from app.post.models import Post
from app.user.models import User
from app.user.decorators import login_required

rating_api = api.namespace('ratings', description='Rates for posts by users')

@rating_api.route('/post')
class PostRatings(Resource):
	@rating_api.expect(authorization, post_rating_model)
	@login_required
	def post(self):
		"""
		Rate a post
		"""
		data = api.payload
		rating_value = data.get("value")
		if rating_value > 5 or rating_value < 0:
			abort(400, {"Value": "The rating value must be between 0 et 5!"})
		post_id = data.get("post_id")
		user_id = g.user.id 
		post = Post.query.get(post_id)
		if not post:
			abort(404)

		rating = PostRating.query.filter_by(user_id=user_id, post_id=post.id).first()
		if rating:
			rating.value = rating_value
		else:
			rating = PostRating(value=rating_value,user_id=user_id,post_id=post_id)
		db.session.add(rating)
		db.session.commit()

		return {"element": post.to_json()},201

	@rating_api.expect(authorization, post_rating_parser)
	@login_required
	def get(self):
		"""
		get user's rating for a post
		"""
		post_id = rating_parser.parse_args()['post_id']
		user_id = g.user.id
		rating = PostRating.query.filter_by(user_id=user_id, post_id=post_id).first()
		if not rating:
			abort(404)
		return {"element": rating.to_json()}

@rating_api.route('/user')
class UserRatings(Resource):
	@rating_api.expect(authorization, user_rating_model)
	@login_required
	def post(self):
		"""
		Rate a user
		"""
		data = api.payload
		rating_value = data.get("value")
		if rating_value > 5 or rating_value < 0:
			abort(400, {"Value": "The rating value must be between 0 et 5!"})
		rated_user_id = data.get("rated_user_id")
		user_id = g.user.id 
		user = User.query.get(rated_user_id)
		if not user:
			abort(404)

		rating = UserRating.query.filter_by(user_id=user_id, rated_user_id=rated_user_id).first()
		if rating:
			rating.value = rating_value
		else:
			rating = UserRating(value=rating_value,user_id=user_id,rated_user_id=rated_user_id)
		db.session.add(rating)
		db.session.commit()

		return {"element": user.to_json()},201

	@rating_api.expect(authorization, user_rating_parser)
	@login_required
	def get(self):
		"""
		get user's rating for an other user
		"""
		rated_user_id = user_rating_parser.parse_args()['rated_user_id']
		user_id = g.user.id
		rating = UserRating.query.filter_by(user_id=user_id, rated_user_id=rated_user_id).first()
		if not rating:
			abort(404)
		return {"element": rating.to_json()}