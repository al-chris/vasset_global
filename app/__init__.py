from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from celery import Celery
from flask_migrate import Migrate
from flask_moment import Moment
from .utils.middleware import set_access_control_allows, check_emerge, json_check, ping_url
from config import Config, configure_logging, config_by_name


from .extensions import db, mail, limiter

# Initialize Flask app
def create_app(config_name=Config.ENV):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Configure JWT
    # app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    jwt = JWTManager(app)

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
    
    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/*": {"origins": Config.CLIENT_ORIGINS}}, supports_credentials=True)

    # Use the after_request decorator to set Access-Control-Allow
    app.after_request(set_access_control_allows)
    
    #app.before_request(ping_url)
    app.before_request(check_emerge)
    # app.before_request(json_check)
    
    
    # Configure logging
    configure_logging(app)

    from .routes import api
    app.register_blueprint(api)

    return app


# For testing
def create_test_app():
    app = create_app('config.TestingConfig')
    return app