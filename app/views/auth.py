'''
This module defines the controller methods for authentication operations in the Trendit³ Flask application.

It includes methods for checking username, checking email, signing up, resending email verification code, and logging in.

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''

import logging
from datetime import datetime, timedelta
from flask import request, make_response, jsonify, current_app
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError, DecodeError
import pyotp

from app.extensions import db
from app.models import User, TempUser, Role, RoleNames, Address, Identification, IdentificationType, Profile, OneTimeToken, NextOfKin, UserSettings
from app.utils.helpers.auth_helpers import generate_six_digit_code, save_pwd_reset_token, send_2fa_code
from app.utils.helpers.email_helpers import send_code_to_email, send_other_emails, EmailType
from app.utils.helpers.basic_helpers import log_exception, console_log
from app.utils.helpers.user_helpers import get_vasset_user, is_email_exist, is_user_exist
from app.utils.helpers.media_helpers import save_media
from app.utils.response import error_response, success_response



class AuthController:

    @staticmethod
    def signup():
        try:
            data = request.get_json()
            email = data.get('email', '')
            username = data.get('username', '')
            password = data.get('password', '')

            if User.query.filter_by(username=username).first():
                return error_response('Username already taken', 409)
            
            if User.query.filter_by(email=email).first():
                return error_response('Email already taken', 409)
                        
            # Check if any field is empty
            if not all([username, password]):
                return {"error": "A required field is not provided."}, 400
            
            
          
            new_user = User(email=email, username=username)

            new_user.password = password
            
            new_user_profile = Profile(vasset_user=new_user)

            # if isinstance(profile_picture, FileStorage) and profile_picture.filename != '':
            #     try:
            #         profile_picture_id = save_media(profile_picture) # This saves image file, saves the path in db and return the id of the image
            #     except Exception as e:
            #         current_app.logger.error(f"An error occurred while profile image: {str(e)}")
            #         return error_response(f"An error occurred saving profile image: {str(e)}", 400)
            # elif profile_picture == '' and new_user:
            #     if new_user_profile.profile_picture_id:
            #         profile_picture_id = new_user_profile.profile_picture_id
            #     else:
            #         profile_picture_id = None
            # else:
            #     profile_picture_id = None

            # new_user_profile.update(profile_picture_id=profile_picture_id)
                        
            new_user_address = Address(vasset_user=new_user)

            new_user_identification = Identification(vasset_user=new_user)

            new_user_setting = UserSettings(vasset_user=new_user)
            
            role = Role.query.filter_by(name=RoleNames.CUSTOMER).first()
            if role:
                new_user.roles.append(role)
            
            new_user_next_of_kin = NextOfKin(vasset_user=new_user)

            db.session.add_all([
                new_user,
                new_user_profile,
                new_user_address, 
                new_user_identification, 
                new_user_next_of_kin,
                new_user_setting
            ])
            db.session.commit()            
            
            user_data = new_user.to_dict()

            # Generate a random six-digit number
            verification_code = generate_six_digit_code()
            
            try:
                send_code_to_email(email, verification_code) # send verification code to user's email
            except Exception as e:
                logging.exception(f"Error sending Email: {str(e)}")
                return error_response(f'An error occurred while sending the verification email: {str(e)}', 500)

            identity = {
                'id': new_user.id,
                'email': email,
                'verification_code': verification_code
            }
            
            # create access token.
            access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=1440), additional_claims={'type': 'access'})
            
            extra_data = {
                'user_data': user_data,
                'access_token': access_token
            }
            
            
            # Send Welcome Email
            try:
                send_other_emails(email, email_type='welcome') # send Welcome message to user's email
            except Exception as e:
                logging.exception(f"Error sending Email: {str(e)}")
                return error_response(f'An error occurred while sending the verification email: {str(e)}', 500)
            
            return success_response('Registration completed successfully', 200, extra_data)

        except IntegrityError as e:
            db.session.rollback()
            log_exception('Integrity Error:', e)
            return error_response(f'User already exists: {str(e)}', 409)
        except (DataError, DatabaseError) as e:
            db.session.rollback()
            log_exception('Database error occurred during registration', e)
            return error_response('Error interacting to the database.', 500)
        except Exception as e:
            db.session.rollback()
            log_exception('An error occurred during registration', e)
            return error_response(f'An error occurred while processing the request: {str(e)}', 500)
        finally:
            db.session.close()

    
    @staticmethod
    def verify_email():
        error = False
        try:
            data = request.get_json()
            signup_token = data.get('signup_token')
            entered_code = data.get('entered_code')
            
            # Decode the JWT and extract the user's info and the verification code
            decoded_token = decode_token(signup_token)
            user_info = decoded_token['sub']
            email = user_info['email']
            
            if int(entered_code) != int(user_info['verification_code']):
                return error_response('Verification code is incorrect', 400)
            
            # The entered code matches the one in the JWT, so create temporary user (TempUser)
            
            # first check if user exists.
            user = User.query.filter_by(email=email).first()
            if user:
                user.email_verified = True
                db.session.commit()
                return success_response('User registered successfully', 201, {'user_data': user.to_dict()})
            
                                    
            user_data = user.to_dict()
            extra_data = {'user_data': user_data}
            
            # # TODO: Make asynchronous
            # if 'referral_code' in user_info:
            #     referral_code = user_info['referral_code']
            #     referrer = get_vasset_user(referral_code)
            #     referral_history = ReferralHistory.create_referral_history(email=email, status='pending', vasset_user=referrer, date_joined=new_user.date_joined)
            
            return success_response('User registered successfully', 201, extra_data)
        except ExpiredSignatureError as e:
            log_exception('Expired Signature Error', e)
            return error_response('The verification code has expired. Please request a new one.', 401)
        except JWTDecodeError as e:
            log_exception('JWT Decode Error', e)
            return error_response('Verification code has expired or corrupted. Please request a new one.', 401)
        except DecodeError as e:
            log_exception('JWT Decode Error', e)
            return error_response('Signup token invalid or corrupted. Make sure you are sending it correctly.', 401)
        except IntegrityError as e:
            db.session.rollback()
            logging.exception(f"Integrity Error: \n {e}")
            return error_response('User already exists.', 409)
        except (DataError, DatabaseError) as e:
            db.session.rollback()
            log_exception('Database error occurred during registration', e)
            return error_response('Error connecting to the database.', 500)
        except Exception as e:
            db.session.rollback()
            log_exception('Exception occurred during registration', e)
            return error_response(f'An error occurred while processing the request: {str(e)}', 500)
        finally:
            db.session.close()


    @staticmethod
    def resend_email_verification_code():
        error = False
        
        try:
            data = request.get_json()
            signup_token = data.get('signup_token')
            
            # Decode the JWT and extract the user's info and the verification code
            decoded_token = decode_token(signup_token)
            user_info = decoded_token['sub']
            email = user_info['email']
            
            # Generate a random six-digit number
            new_verification_code = generate_six_digit_code()
            
            user_info.update({'verification_code': new_verification_code})
            
            try:
                send_code_to_email(email, new_verification_code) # send verification code to user's email
            except Exception as e:
                logging.exception(f"Error sending Email: {str(e)}")
                return error_response(f'Try again. An error occurred resending the verification email: {str(e)}', 500)
            
            # Create a JWT that includes the user's info and the verification code
            expires = timedelta(minutes=30)
            signup_token = create_access_token(identity=user_info, expires_delta=expires, additional_claims={'type': 'signup'})
            extra_data = {'signup_token': signup_token}
            
        except ExpiredSignatureError as e:
            error = True
            msg = f"The Signup token has expired. Please try signing up again."
            status_code = 401
            logging.exception(f"Expired Signature Error: {e}")
        except JWTDecodeError as e:
            error = True
            msg = f"The Signup token has expired or corrupted. Please try signing up again."
            status_code = 401
            logging.exception(f"JWT Decode Error: {e}")
        except Exception as e:
            error = True
            status_code = 500
            msg = 'An error occurred trying to resend verification code.'
            logging.exception(f"An exception occurred resending verification code. {e}") # Log the error details for debugging
        if error:
            return error_response(msg, status_code)
        else:
            return success_response('New Verification code sent successfully', 200, extra_data)
        
    @staticmethod
    def login():
        
        try:
            data = request.get_json()
            email_username = data.get('email_username')
            pwd = data.get('password')
            
            # get user from db with the email/username.
            user = get_vasset_user(email_username)
            
            if not user:
                return error_response('Email/username is incorrect or doesn\'t exist', 401)
            
            if not user.verify_password(pwd):
                return error_response('Password is incorrect', 401)
            
            
            # Check if user has enabled 2FA
            user_settings = user.user_settings
            user_security_setting = user_settings.security_setting
            two_factor_method = user_security_setting.two_factor_method if user_security_setting else None
            
            
            identity={
                'username': user.username,
                'email': user.email,
                # 'two_factor_method': two_factor_method.value
            }

            if not user_settings or not two_factor_method:
                access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=1440), additional_claims={'type': 'access'})
                user_data = user.to_dict()
                extra_data = {'access_token': access_token, 'user_data': user_data}
                msg = 'Logged in successfully'

            elif user_security_setting and two_factor_method.value in ['email', 'phone']:
                # Generate 2FA code and send it to the user
                two_FA_code = generate_six_digit_code()
                
                try:
                    send_2fa_code(user, two_factor_method.value, two_FA_code)
                except Exception as e:
                    return error_response(f'An error occurred sending the 2FA code', 500)
                
                # Create a JWT that includes the user's info and the 2FA code
                expires = timedelta(minutes=15)
                identity.update({'two_FA_code': two_FA_code})
                two_FA_token = create_access_token(identity=identity, expires_delta=expires, additional_claims={'type': '2fa'})
                extra_data = { 'two_FA_token': two_FA_token }
                msg = '2 Factor Authentication code sent successfully'

            elif user_security_setting and two_factor_method.value == 'google auth app':
                expires = timedelta(minutes=30)
                two_FA_token = create_access_token(identity=identity, expires_delta=expires, additional_claims={'type': '2fa'})
                extra_data = { 'two_FA_token': two_FA_token }
                msg = 'Check the Google Auth App for 2 Factor Authentication code.'
            
            api_response = success_response(msg, 200, extra_data)
        
        except UnsupportedMediaType as e:
            logging.exception(f"An UnsupportedMediaType exception occurred: {e}")
            api_response = success_response(f"{str(e)}", 415)
        except Exception as e:
            logging.exception(f"An exception occurred trying to login: {e}")
            api_response = success_response(f'An Unexpected error occurred processing the request.', 500)
        finally:
            db.session.close()
        
        return api_response
    
    @staticmethod
    def forgot_password():
        error = False
        
        try:
            data = request.get_json()
            email_username = data.get('email_username')
            
            # get user from db with the email/username.
            user = get_vasset_user(email_username)
            
            if not user:
                return error_response('email or username isn\'t registered with us', 404)
            
            # Generate a random six-digit number
            reset_code = generate_six_digit_code()
            
            try:
                send_code_to_email(user.email, reset_code, code_type=EmailType.PWD_RESET) # send reset code to user's email
            except Exception as e:
                return error_response(f'An error occurred while sending the reset code to the email address', 500)
            
            # Create a JWT that includes the user's info and the reset code
            expires = timedelta(minutes=15)
            reset_token = create_access_token(identity={
                'username': user.username,
                'email': user.email,
                'reset_code': reset_code
            }, expires_delta=expires)
            
            pwd_reset_token = save_pwd_reset_token(reset_token, user)
            
            if pwd_reset_token is None:
                return error_response('Error saving the reset token in the database', 500)
            
            status_code = 200
            msg = 'Password reset code sent successfully'
            extra_data = { 'reset_token': reset_token, 'email': user.email, }
            return success_response(msg, status_code, extra_data)

        except Exception as e:
            status_code = 500
            msg = 'An error occurred while processing the request.'
            log_exception(f"An exception occurred processing the request", e)
            return error_response(msg, status_code)
        finally:
            db.session.close()


    @staticmethod
    def reset_password():
        
        try:
            data = request.get_json()
            reset_token = data.get('reset_token')
            entered_code = data.get('entered_code')
            new_password = data.get('new_password')
            # hashed_pwd = generate_password_hash(new_password, "pbkdf2:sha256")
            
            try:
                # Decode the JWT and extract the user's info and the reset code
                decoded_token = decode_token(reset_token)
                if not decoded_token:
                    return error_response('Invalid or expired reset code', 401)
                
                token_data = decoded_token['sub']
            except ExpiredSignatureError:
                return error_response("The reset code has expired. Please request a new one.", 401)
            except Exception as e:
                return error_response("An error occurred while processing the request.", 500)
            
            
            # Check if the reset token exists in the database
            pwd_reset_token = OneTimeToken.query.filter_by(token=reset_token).first()
            if not pwd_reset_token:
                return error_response('The Reset token not found.', 404)
            
            if pwd_reset_token.used:
                return error_response('The Reset Code has already been used', 403)
            
            # Check if the entered code matches the one in the JWT
            if int(entered_code) != int(token_data['reset_code']):
                return error_response('The wrong password Reset Code was provided. Please check your mail for the correct code and try again.', 400)
            
            # Reset token is valid, update user password
            # get user from db with the email.
            user = get_vasset_user(token_data['email'])
            user.password = new_password
            
            # Reset token is valid, mark it as used
            pwd_reset_token.update(used=True)
            status_code = 200
            msg = 'Password changed successfully'
            return success_response(msg, status_code)
        
        except UnsupportedMediaType as e:
            db.session.rollback()
            logging.exception(f"An UnsupportedMediaType exception occurred: {e}")
            return error_response(f"{str(e)}", 415)
        except JWTDecodeError:
            db.session.rollback()
            return error_response(f"Invalid or expired reset code", 401)
        except Exception as e:
            db.session.rollback()
            logging.exception(f"An exception occurred processing the request: {e}")
            return error_response('An error occurred while processing the request.', 500)
        finally:
            db.session.close()


    @staticmethod
    def logout():
        try:
            resp = make_response(success_response('User logged out successfully', 200))
            return resp
        except Exception as e:
            resp = make_response(error_response(f'Log out failed: {e}', 500))
            return resp
    
    
    @staticmethod
    def delete_account():
        try:
            current_user_id = get_jwt_identity()
            
            if current_user_id is None:
                return error_response('Invalid user identity', 401)
            
            current_user = User.query.get(current_user_id)
            
            if not current_user:
                return error_response('User not found', 404)

            # Uncomment if password verification is required
            # data = request.get_json()
            # pwd = data.get('password', '')
            # if not pwd:
            #     return error_response('Password is required', 400)
            # if not current_user.verify_password(pwd):
            #     return error_response('Password is incorrect', 401)
            
            # Proceed with account deletion
            db.session.delete(current_user)
            db.session.commit()
            
            api_response = success_response('Account deleted successfully', 200)
            
        except Exception as e:
            db.session.rollback()
            logging.exception(f"An exception occurred processing request: {e}")
            api_response = error_response('An unexpected error occurred while processing the request.', 500)
        finally:
            db.session.close()
        
        return api_response
    
    
    
    @staticmethod
    def username_check():
        error = False
        try:
            data = request.get_json()
            username = data.get('username', '')
            if not username:
                return error_response("username parameter is required in request's body.", 400)
            
            if is_user_exist(username, 'username'):
                return error_response(f'{username} is already Taken', 409)
            
            msg = f'{username} is available'
            status_code = 200
            
        except UnsupportedMediaType as e:
            error = True
            msg = "username parameter is required in request's body."
            status_code = 415
            logging.exception(f"An exception occurred checking username. {e}")
        except Exception as e:
            error = True
            msg = "An error occurred while processing the request."
            status_code = 500
            logging.exception(f"An exception occurred checking username. {e}")
        
        return error_response(msg, status_code) if error else success_response(msg, status_code)
    
    
    @staticmethod
    def email_check():
        error = False
        try:
            data = request.get_json()
            email = data.get('email', '')
            if not email:
                return error_response("email parameter is required in request's body.", 415)
            
            if is_user_exist(email, 'email'):
                return error_response(f'{email} is already taken', 409)
            
            msg = f'{email} is available'
            status_code = 200
            
        except UnsupportedMediaType as e:
            error = True
            msg = "email parameter is required in request's body."
            status_code = 415
            logging.exception(f"An exception occurred checking email. {e}")
        except Exception as e:
            error = True
            msg = "An error occurred while processing the request."
            status_code = 500
            logging.exception(f"An exception occurred checking email. {e}")

        return error_response(msg, status_code) if error else success_response(msg, status_code)
    
    