from flask_smorest import Blueprint

bp = Blueprint('users',__name__, description= 'ops on users')

from . import routes
from . import auth_routes
