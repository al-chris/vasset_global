'''
This module defines the configuration settings for the Trendit³ Flask application.

It includes configurations for the environment, database, JWT, Paystack, mail, Cloudinary, and Celery. 
It also includes a function to configure logging for the application.

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''
import os, secrets, logging
from datetime import timedelta
from celery import Celery



class Config:
    # other app configurations
    ENV = os.environ.get('ENV') or 'development'
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://vasset_user:EpXJqNOltaTSKKX50BcBI0eO55xoNtb3@dpg-cockceq1hbls73cshk1g-a/vasset'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = (ENV == 'development')  # Enable debug mode only in development
    STATIC_DIR = 'app/static'
    UPLOADS_DIR = 'app/static/uploads'
    EMERGENCY_MODE = os.environ.get('EMERGENCY_MODE') or False
    DOMAIN_NAME = os.environ.get('DOMAIN_NAME') or 'https://www.vassetglobal.com'
    API_DOMAIN_NAME = os.environ.get('API_DOMAIN_NAME') or 'https://api.vassetglobal.com'
    CLIENT_ORIGINS = os.environ.get('CLIENT_ORIGINS') or 'http://localhost:3000,http://localhost:5173,https://trendit3.vercel.app'
    CLIENT_ORIGINS = [origin.strip() for origin in CLIENT_ORIGINS.split(',')]
    
    # Constants
    TASKS_PER_PAGE = os.environ.get('TASKS_PER_PAGE') or 10
    ITEMS_PER_PAGE = os.environ.get('ITEMS_PER_PAGE') or 10
    PAYMENT_TYPES = ['task-creation', 'membership-fee', 'credit-wallet', 'item-upload']
    
    # JWT configurations
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or "super-secret" # Change This
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


    ADMIN_ID = os.environ.get('ADMIN_ID') or 35
    
    
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Cloudinary configurations
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or "drmw6zdyg"
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or "825665579274186"
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or "bEjMIYzt-H8xGWSAbIUZlfDG4zY"
    
    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    CELERY_ACCEPT_CONTENT = ['application/json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'


    # Google config
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # Facebook config
    FB_CLIENT_ID = os.environ.get('FB_CLIENT_ID')
    FB_CLIENT_SECRET = os.environ.get('FB_CLIENT_SECRET')
    FB_REDIRECT_URI = os.environ.get('FB_REDIRECT_URI')

    # TikTok config


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    DEBUG_TOOLBAR = True  # Enable debug toolbar
    EXPOSE_DEBUG_SERVER = False  # Do not expose debugger publicly

class ProductionConfig(Config):
    DEBUG = False
    FLASK_DEBUG = False
    DEBUG_TOOLBAR = False
    EXPOSE_DEBUG_SERVER = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False  # Typically disabled during testing


# Map config based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}

def configure_logging(app):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)  # Set the desired logging level
