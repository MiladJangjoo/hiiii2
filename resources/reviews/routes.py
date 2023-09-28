from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from schemas import ReviewSchema
from . import bp
from db import reviews



@bp.route('/')
class ReviewList(MethodView):
    def get(self):
        return {'reviews': reviews}, 200

    @bp.arguments(ReviewSchema)
    def post(self, review_data):
        reviews[uuid4().hex] = review_data
        return review_data, 201


@bp.route('/<review_id>')
class Review(MethodView):
    def get(self,review_id):
        try:
            review = reviews[review_id]
            return review, 200
        except:
            abort(404, message = 'review not found ')
            
    @bp.arguments(ReviewSchema)
    def put(self , review_data, review_id):
        if review_id in reviews:
            review= reviews[review_id]
            if review_data['user_id'] != review['user_id']:
                abort(400,message = 'cannot edit the review')   
            review['body'] = review_data['body']
            return review, 200
        abort(404,message= 'review not found')


    def delete(self,review_id):
        try:
            deleted_review = reviews.pop(review_id)
            return {'messege': f'{deleted_review["body"]} deleted'}
        except:
            
            abort(404,message= 'review not found')