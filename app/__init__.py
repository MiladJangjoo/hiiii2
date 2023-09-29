from flask import Flask
from flask_smorest import Api
from Config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)


db= SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

from resources.users import bp as user_bp
api.register_blueprint(user_bp)
from resources.reviews import bp as review_bp
api.register_blueprint(review_bp)

from resources.users import routes
from resources.reviews import routes
from resources.users.models import UserModel
from resources.reviews.ReviewModel import ReviewModel

