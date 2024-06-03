'''
This module defines helper functions for managing users in the VASSET Flask application.

These functions assist with tasks such as:
    * fetching user info
    * checking if username or email exist
    * generating referral code. e.t.c...

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''
from flask import current_app
from threading import Thread
from ...extensions import db
from ...models.user import User, Address, Profile
from ...utils.helpers.basic_helpers import generate_random_string, log_exception
from ...utils.helpers.media_helpers import save_media
from werkzeug.datastructures import FileStorage


def async_save_id_img(app, user: User, media_file):
    with app.app_context():
        try:
            user_identification = user.identification
            if isinstance(media_file, FileStorage) and media_file.filename != '':
                try:
                    identification_image = save_media(media_file) # This saves image file, saves the path in db and return the Media instance
                except Exception as e:
                    log_exception(f"An error occurred saving profile image: {str(e)}")
            elif identification_image == '' and user:
                if user_identification.profile_picture_id:
                    identification_image = user_identification.profile_picture
                else:
                    identification_image = None
            else:
                identification_image = None
            
            user_identification.update(identification_pic=identification_image)
        except Exception as e:
            log_exception()
            raise e

def save_id_img(user: User, media_file: FileStorage):
    Thread(target=async_save_id_img, args=(current_app._get_current_object(), user, media_file)).start()


def async_save_profile_pic(app, user: User, media_file):
    with app.app_context():
        try:
            user_profile = user.profile
            if isinstance(media_file, FileStorage) and media_file.filename != '':
                try:
                    profile_picture = save_media(media_file) # This saves image file, saves the path in db and return the Media instance
                except Exception as e:
                    log_exception(f"An error occurred saving profile image: {str(e)}")
            elif profile_picture == '' and user:
                if user_profile.profile_picture_id:
                    profile_picture = user_profile.profile_picture
                else:
                    profile_picture = None
            else:
                profile_picture = None
            
            user_profile.update(profile_picture=profile_picture)
        except Exception as e:
            log_exception()
            raise e

def save_profile_pic(user: User, media_file: FileStorage):
    Thread(target=async_save_profile_pic, args=(current_app._get_current_object(), user, media_file)).start()


def get_user_info(userId):
    '''Gets profile details of a particular user'''
    
    if userId is None:
        userInfo = {}
    else:
        vasset_user = User.query.filter(User.id == userId).first()
        userInfo = vasset_user.to_dict()
    
    for key in userInfo:
        if userInfo[key] is None:
            userInfo[key] = ''
    
    return userInfo


def is_user_exist(identifier, field, user=None):
    """
    Checks if a user exists in the database with the given identifier and field.

    Args:
        identifier: The identifier to search for (email or username).
        field: The field to search in ("email" or "username").
        user: An optional user object. If provided, the check excludes the user itself.

    Returns:
        True if the user exists, False otherwise.
    """
    base_query = User.query.filter(getattr(User, field) == identifier)
    if user:
        base_query = base_query.filter(User.id != user.id)
    return base_query.scalar() is not None

def is_username_exist(username, user=None):
    """
    Checks if a username exists in the database, excluding the current user if provided.

    Args:
        username: The username to search for.
        user: An optional user object. If provided, the check excludes the user itself.

    Returns:
        True if the username is already taken, False if it's available.
    """
    base_query = User.query.filter(User.username == username)
    if user:
        # Query the database to check if the username is available, excluding the user's own username
        base_query = base_query.filter(User.id != user.id)
    
    return base_query.scalar() is not None


def is_email_exist(email, user=None):
    """
    Checks if an email address exists in the database, excluding the current user if provided.

    Args:
        email: The email address to search for.
        user: An optional user object. If provided, the check excludes the user itself.

    Returns:
        True if the email address is already taken, False if it's available.
    """
    base_query = User.query.filter(User.email == email)
    if user:
        # Query the database to check if the email is available, excluding the user's own email
        base_query = base_query.filter(User.id != user.id)
    
    return base_query.scalar() is not None


def get_vasset_user(email_username):
    """
    Retrieves a User object from the database based on email or username.

    Args:
        email_username: The email address or username to search for.

    Returns:
        The User object if found, or None if not found.
    """
    
    user = User.query.filter(User.email == email_username).first()
    if user:
        return user
    
    return User.query.filter(User.username == email_username).first()


def get_vasset_user_by_google_id(google_id):
    """
    Retrieves a User object from the database based on social ID.

    Args:
        social_id: The social ID to search for.

    Returns:
        The User object if found, or None if not found.
    """
    return User.query.filter(User.social_ids.google_id == google_id).first()


def get_vasset_user_by_facebook_id(facebook_id):
    """
    Retrieves a User object from the database based on social ID.

    Args:
        social_id: The social ID to search for.

    Returns:
        The User object if found, or None if not found.
    """
    return User.query.filter(User.social_ids.facebook_id == facebook_id).first()


def get_vasset_user_by_x_id(x_id):
    """
    Retrieves a User object from the database based on social ID.

    Args:
        social_id: The social ID to search for.

    Returns:
        The User object if found, or None if not found.
    """
    return User.query.filter(User.social_ids.x_id == x_id).first()


def get_vasset_user_by_tiktok_id(tiktok_id):
    """
    Retrieves a User object from the database based on social ID.

    Args:
        social_id: The social ID to search for.

    Returns:
        The User object if found, or None if not found.
    """
    return User.query.filter(User.social_ids.tiktok_id == tiktok_id).first()

def generate_referral_code(length=6):
    while True:
        code = generate_random_string(length)
        # Check if the code already exists in the database
        if not referral_code_exists(code):
            return code

def referral_code_exists(code):
    profile = Profile.query.filter(Profile.referral_code == code).first()
    if profile:
        return True
    return False

