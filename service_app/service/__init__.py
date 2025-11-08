from flask import Blueprint

bp = Blueprint('service', __name__)

from service_app.service import routes
