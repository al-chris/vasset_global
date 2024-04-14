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
from app.utils.response import error_response, success_response



class AuthController:

    @staticmethod
    def signup():
        try:
            data = request.get_json()
            email = data.get('email', '')
            username = data.get('username', '')
            password = data.get('password', '')
            country = data.get('country', '')
            address = data.get('address', '')
            state = data.get('state', '')
            city = data.get('city', '')
            currency_code = data.get('currency_code', '')
            postal_code = data.get('postal_code', '')
            firstname = data.get('firstname', '')
            lastname = data.get('lastname', '')
            gender = data.get('gender', '')
            phone = data.get('phone', '')
            birthday = data.get('birthday', '')
            profile_picture_id = data.get('profile_picture_id', '')
            id_type = data.get('id_type', '')
            id_issue_date = data.get('id_issue_date', '')
            id_expiration_date = data.get('id_expiration_date', '')
            id_picture = data.get('id_picture', '')
            bvn = data.get('bvn', '')

            if User.query.filter_by(username=username).first():
                return error_response('Username already taken', 409)
            
            if User.query.filter_by(email=email).first():
                return error_response('Email already taken', 409)

            pass

        except Exception as e:
            pass