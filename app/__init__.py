from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from flask_migrate import Migrate
from flask_moment import Moment


from .extensions import db, mail, limiter

# Initialize Flask app
def create_app():
    app = Flask(__name__)

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    jwt = JWTManager(app)

    # Enable CORS
    CORS(app)

    # Initialize Celery
    celery = Celery(app.name, broker='redis://localhost:6379/0')
    celery.conf.update(app.config)

    db.init_app(app)
    mail.init_app(app) # Initialize Flask-Mail
    limiter.init_app(app) # initialize rate limiter 

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize Flask-Moment
    moment = Moment(app)

    # Add your app routes and other configurations here

    return app