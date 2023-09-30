from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from resources.users.models import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity

from .ReviewModel import ReviewModel
from schemas import ReviewSchema
from . import bp




@bp.route('/')
class ReviewList(MethodView):

    @jwt_required()
    @bp.response(200,ReviewSchema(many=True))
    def get(self):
        return ReviewModel.query.all()

    @jwt_required()
    @bp.arguments(ReviewSchema)
    @bp.response(200, ReviewSchema)
    def post(self, review_data):
        user_id = get_jwt_identity()
        r = ReviewModel(**review_data, user_id = user_id)
        try:
            r.save()
            return r
        except IntegrityError:
            abort(400, message = 'invalid user id')


@bp.route('/<review_id>')
class Review(MethodView):
    
    @jwt_required()
    @bp.response(200, ReviewSchema)
    def get(self,review_id):
      r = ReviewModel.query.get(review_id) 
      if r:
          return r 
      abort(400, message ='invalid review id')

    @jwt_required()       
    @bp.arguments(ReviewSchema)
    @bp.response(200, ReviewSchema)
    def put(self , review_data, review_id):
        r = ReviewModel.query.get(review_id)
        if r and review_data['body']:
            user_id = get_jwt_identity()
            if r.user_id == user_id:
                r.body = review_data['body']
                r.save()
                return r
            else:
                abort(401, message = 'unautorize')
        abort(400, message= 'invalid review data')
             

    @jwt_required()
    def delete(self,review_id):
        user_id = get_jwt_identity()
        r = ReviewModel.query.get(review_id)
        if r:
            if r.user_id == user_id:
                r.delete()
                return {'message' : 'post deleted'}, 200
            abort(400, message= 'user doesnt have rights to do this')
        abort(400, message = 'invalid review id')
