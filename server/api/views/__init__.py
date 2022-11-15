from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api')
from api.views.users import *
from api.views.interests import *
from api.views.connections import *
from api.views.messages import *