from flask_smorest import Blueprint

bp = Blueprint('reviews', __name__, url_prefix='/review')

from . import routes