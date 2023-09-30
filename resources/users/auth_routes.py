from flask_smorest import abort
from schemas import AutheuserSchema, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from . import bp
from .models import UserModel


@bp.post('/register')
@bp.arguments(UserSchema)
@bp.response(201, UserSchema)
def register(user_data):
    user = UserModel()
    user.from_dict(user_data)
    try:
        user.save()
        return user_data
    except IntegrityError:
        abort(400, message= "username or email already taken")


@bp.post('/login')
@bp.arguments(AutheuserSchema)
def login(login_info):
    if 'username' not in login_info and 'email' not in login_info:
        abort(400, message= 'please include user name or email')
    if 'username' in login_info:
        user = UserModel.query.filter_by(username = login_info['username']).first()
    else:
        user = UserModel.query.filter_by(email = login_info['email']).first()
    if user and user.check_password(login_info['password']):
        access_token = create_access_token(identity=user.id)
        return {'access_token' : access_token}
    abort(400, message= "uinvalid username or password")




# @bp.route('/logout')