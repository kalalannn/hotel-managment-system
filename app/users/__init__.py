from flask import Blueprint

users = Blueprint('users', __name__)

from . import controllers, forms
