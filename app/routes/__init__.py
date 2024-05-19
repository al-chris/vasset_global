'''
This package contains the API routes for the VASSET Flask application.

It includes routes for Vasset.

A Flask blueprint named 'api' is created to group these routes, and it is registered under the '/api' URL prefix.

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''
from flask import Blueprint, render_template

api = Blueprint('api', __name__, url_prefix='/api')

from . import auth, profile

@api.route("/", methods=['GET'])
def index():
    return render_template('api/index.jinja-html')