from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import UplateUserSchema, UserSchema, ReviewSchema, DeleteuserSchema
from . import bp
from .UserModel import UserModel

from db import users, reviews


@bp.route('/user')
class UserList(MethodView):
    @bp.response(200, UserSchema( many = True))
    def get(self):
        users = UserModel.query.all()
        return users

    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel()
        user.from_dict(user_data)
        try:
            user.save()
            return user_data
        except IntegrityError:
            abort(400, message= "username or email already taken")

    @bp.arguments(DeleteuserSchema)
    def delete(self, user_data):
        user= UserModel.query.filter_by(username = user_data['username']).first()
        if user and user.check_password(user_data['password']):
            user.delete()
            return {'message' : f'{user_data["username"]} deleted'},202
        abort(400,message ='username or password invalid')


@bp.route('/user/<user_id>')
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
      return UserModel.query.get_or_404(user_id, description='user not found')
      
    
    @bp.arguments(UplateUserSchema)
    @bp.response(202, UserSchema)    
    def put(self,user_data, user_id):
        user = UserModel.query.get_or_404(user_id, description='user not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message = 'username or email already taken')
        



@bp.get('/user/<user_id>/review')
@bp.response(200, ReviewSchema(many = True))
def get_user_review(user_id):
    if user_id not in users:
        abort(404,message= 'user not found')
        
    user_reviews = [review for review in reviews.values() if review['user_id'] == user_id]
    return user_reviews, 200