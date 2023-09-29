from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from resources.users.models import UserModel

from .ReviewModel import ReviewModel
from schemas import ReviewSchema
from . import bp




@bp.route('/')
class ReviewList(MethodView):
    @bp.response(200,ReviewSchema(many=True))
    def get(self):
        return ReviewModel.query.all()

    @bp.arguments(ReviewSchema)
    @bp.response(200, ReviewSchema)
    def post(self, review_data):
        r = ReviewModel(**review_data)
        u =UserModel.query.get(review_data['user_id'])
        if u:
            r.save()
            return r
        else:
            abort(400, message = 'invalid user id')


@bp.route('/<review_id>')
class Review(MethodView):
    
    @bp.response(200, ReviewSchema)
    def get(self,review_id):
      r = ReviewModel.query.get(review_id) 
      if r:
          return r 
      abort(400, message ='invalid review id')
            
    @bp.arguments(ReviewSchema)
    @bp.response(200, ReviewSchema)
    def put(self , review_data, review_id):
        r = ReviewModel.query.get(review_id)
        if r and review_data['body']:
            if r.user_id == review_data['user_id']:
                r.body = review_data['body']
                r.save()
                return r
        abort(400, message= 'invalid review data')
             


    def delete(self,review_id):
        req_data = request.get_json()
        user_id = req_data['user_id']
        r = ReviewModel.query.get(review_id)
        if r:
            if r.user_id == user_id:
                r.delete()
                return {'message' : 'post deleted'}, 200
            abort(400, message= 'user doesnt have rights to do this')
        abort(400, message = 'invalid review id')
