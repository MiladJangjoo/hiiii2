
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from schemas import UplateUserSchema, UserSchema, ReviewSchema, AutheuserSchema, UserSchemaNested
from . import bp
from .models import UserModel

from db import users, reviews


@bp.route('/user')
class UserList(MethodView):
    @bp.response(200, UserSchema( many = True))
    def get(self):
        users = UserModel.query.all()
        return users

   
    @jwt_required()
    @bp.arguments(AutheuserSchema)
    def delete(self, user_data):
        user_id =get_jwt_identity()
        user = UserModel.query.get(user_id)
        if user and user.username == user_data['username'] and user.check_password(user_data['password']):
            user.delete()
            return {'message' : f'{user_data["username"]} deleted'},202
        abort(400,message ='username or password invalid')


    @jwt_required()
    @bp.arguments(UplateUserSchema)
    @bp.response(202, UserSchema)    
    def put(self,user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id, description='user not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message = 'username or email already taken')


@bp.route('/user/<user_id>')
class User(MethodView):
    
    @bp.response(200, UserSchemaNested)
    def get(self, user_id):
        user = None
        if user_id.isdigit():
            user = UserModel.query.get(user_id)
        else:
            user = UserModel.query.filter_by(username= user_id).first()
        if user:
            return user
        abort(400, message = 'please enter valid username or id')
      
    
        

@bp.route('/user/follow/<followed_id>')
class FollowUser(MethodView):
    
    @jwt_required()
    @bp.response(200, UserSchema(many=True))
    def post(self, followed_id):
        follower_id = get_jwt_identity()    
        user = UserModel.query.get(follower_id)
        user_to_follow = UserModel.query.get(followed_id)
        if user and user_to_follow:
            user.follow_user(user_to_follow)
            return user.followed.all()
        abort(400, message = 'invalid user info')
    
    @jwt_required()
    def put(self,followed_id):
        follower_id = get_jwt_identity()
        user = UserModel.query.get(follower_id)
        user_to_unfollow = UserModel.query.get(followed_id)
        if user and user_to_unfollow:
            user.unfollow_user(user_to_unfollow)
            return {'message': f" user: {user_to_unfollow.username} unfollowed"}, 202
        abort(400, message = 'invalid user info')


