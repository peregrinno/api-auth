from .common import *

api_blueprint = Blueprint('api', __name__, template_folder='templates')

from . import api