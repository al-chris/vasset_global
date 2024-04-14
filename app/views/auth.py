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
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import UnsupportedMediaType
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError, DecodeError
import pyotp

from app.extensions import db
from app.models import User, TempUser, Role, RoleNames, Address, Identification, IdentificationType, Profile, OneTimeToken
from app.utils.helpers.auth_helpers import generate_six_digit_code, save_pwd_reset_token, send_2fa_code
from app.utils.helpers.email_helpers import send_code_to_email, send_other_emails
from app.utils.helpers.basic_helpers import log_exception, console_log
from app.utils.helpers.user_helpers import get_vasset_user
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
                        
            # Check if any field is empty
            if not all([firstname, lastname, username, password]):
                return {"error": "A required field is not provided."}, 400
            
            new_user = User(email=email, username=username)
            new_user.password = password
            new_user_profile = Profile(vasset_user=new_user, firstname=firstname, lastname=lastname)
            new_user_address = Address(vasset_user=new_user)
            # new_user_setting = UserSettings(trendit3_user=new_user)
            role = Role.query.filter_by(name=RoleNames.CUSTOMER).first()
            if role:
                new_user.roles.append(role)
            
            db.session.add_all([new_user, new_user_profile, new_user_address])
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
            #     referral_history = ReferralHistory.create_referral_history(email=email, status='pending', trendit3_user=referrer, date_joined=new_user.date_joined)
            
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