from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from celery import Celery
from celery.schedules import crontab
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config

db = SQLAlchemy()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)

def make_celery(app_name=__name__):
    backend = Config.CELERY_RESULT_BACKEND
    broker = Config.CELERY_BROKER_URL
    return Celery(app_name, backend=backend, broker=broker)

celery = make_celery()
