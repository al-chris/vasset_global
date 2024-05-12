from flask_jwt_extended import jwt_required

from . import api
from app.views import ProfileController


@api.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    return ProfileController.get_profile()

# @api.route('/profile/edit', methods=['POST'])
# @jwt_required()
# def edit_profile():
#     return ProfileController.edit_profile()

@api.route('/profile/update', methods=['POST'])
def update_profile():
    return ProfileController.update_profile()


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

# # bank details
# @api.route("profile/bank", methods=['GET', 'POST'])
# @jwt_required()
# def bank_details():
#     return ProfileController.bank_details()