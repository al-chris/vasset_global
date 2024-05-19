'''
This module defines the routes for authentication operations in the VASSET Flask application.

It includes routes for signing up, verifying email, logging in, verifying 2FA, forgetting password, and resetting password.

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''

from flask import request
from flask_jwt_extended import jwt_required

from . import api

from app.views import AuthController


# REGISTRATION ENDPOINTS
@api.route("/signup", methods=['POST'])
def signUp():
    return AuthController.signup()

@api.route("/verify-email", methods=['POST'])
def verify_email():
    return AuthController.verify_email()


# AUTHENTICATION ENDPOINTS
@api.route("/login", methods=['POST'])
def login():
    return AuthController.login()

@api.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    return AuthController.verify_2fa()


@api.route("/forgot-password", methods=['POST'])
def forgot_password():
    return AuthController.forgot_password()

@api.route("/reset-password", methods=['POST'])
def reset_password():
    return AuthController.reset_password()


@api.route("/resend-code", methods=['POST'])
def resend_code():
    code_type = request.args.get('code_type', 'email-signup')
    
    if code_type == 'email-signup':
        return AuthController.resend_email_verification_code()
    # if code_type == 'email-edit':
    #     return ProfileController.user_email_edit()
    if code_type == 'pwd-reset':
        return AuthController.forgot_password()

@api.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    return AuthController.logout()

@api.route('/delete-account', methods=['DELETE'])
@jwt_required()
def delete_account():
    return AuthController.delete_account()


@api.route('/check-username', methods=['GET'])
def username_check():
    return AuthController.username_check()

@api.route('/check-email', methods=['GET'])
def email_check():
    return AuthController.email_check()