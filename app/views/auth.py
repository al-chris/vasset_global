'''
This module defines the controller methods for authentication operations in the Trendit³ Flask application.

It includes methods for checking username, checking email, signing up, resending email verification code, and logging in.

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''

import logging
from datetime import timedelta
from flask import request, make_response
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import UnsupportedMediaType
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError, DecodeError
import pyotp

from app.extensions import db
from app.models import User, TempUser, Role, RoleNames, Address, Identification, IdentificationType, Profile, OneTimeToken
from app.utils.helpers.auth_helpers import generate_six_digit_code, save_pwd_reset_token, send_2fa_code




class AuthController:

    @staticmethod
    def signup():
        try:
            data = request.get_json()
            email = data.get('email')
            pass

        except Exception as e:
            pass