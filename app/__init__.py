from flask import Flask

app = Flask(__name__)

from resources.users import routes
from resources.reviews import routes