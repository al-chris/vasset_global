'''
This module defines the routes for profile management and authentication operations in the VASSET Flask application.

It includes routes for getting and updating user profiles, updating profile pictures, editing and verifying email, and updating next of kin, identification, and address details.

Routes:
    - /profile (GET): Get user profile information.
    - /profile/update (POST): Update user profile information.
    - /profile/update-nextofkin (POST): Update user's next of kin information.
    - /profile/update-identification (POST): Update user's identification information.
    - /profile/update-address (POST): Update user's address information.
    - /profile-pic (GET): Get user's profile picture.
    - /profile-pic/edit (POST): Update user's profile picture.
    - /profile/email-edit (POST): Edit user's email address.
    - /profile/email-verify (POST): Verify user's email address.

Note: All routes require JWT authentication.

Author:
    Chris
Link:
    https://github.com/al-chris
Package:
    VASSET
'''
from flask_jwt_extended import jwt_required

from . import api
from app.views import ProfileController


@api.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    return ProfileController.get_profile()


@api.route('/profile/update', methods=['POST'])
@jwt_required()
def update_user_profile():
    return ProfileController.update_user_profile()


@api.route('/profile/update-nextofkin', methods=['POST'])
@jwt_required()
def update_nextofkin():
    return ProfileController.update_nextofkin()


@api.route('/profile/update-identification', methods=['POST'])
@jwt_required()
def update_identification():
    return ProfileController.update_identification()


@api.route('/profile/update-address', methods=['POST'])
@jwt_required()
def update_address():
    return ProfileController.update_address()


@api.route('/profile-pic', methods=['GET'])
@jwt_required()
def get_profile_pic():
    return ProfileController.get_profile_pic()

@api.route('/profile-pic/edit', methods=['POST'])
@jwt_required()
def update_profile_pic():
    return ProfileController.update_profile_pic()

@api.route('/profile/email-edit', methods=['POST'])
@jwt_required()
def user_email_edit():
    return ProfileController.user_email_edit()

@api.route('/profile/email-verify', methods=['POST'])
@jwt_required()
def verify_email_edit():
    return ProfileController.verify_email_edit()


@api.route('/profile/balance', methods=['GET'])
@jwt_required()
def get_user_balance():
    return ProfileController.get_user_balance()