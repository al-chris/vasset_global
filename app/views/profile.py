import logging
from datetime import timedelta
from flask import request, jsonify, current_app
from werkzeug.datastructures import FileStorage
from sqlalchemy.exc import ( IntegrityError, DataError, DatabaseError, InvalidRequestError, )
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity, jwt_required, get_jwt, get_jwt_header
from flask_jwt_extended.exceptions import JWTDecodeError

from ..extensions import db
from ..models import User, Address, Profile
from app.models.user import User, Address, Profile
# from ..utils.helpers.location_helpers import get_currency_info
from app.utils.helpers.basic_helpers import console_log, log_exception
from app.utils.helpers.user_helpers import get_user_info
from app.utils.helpers.media_helpers import save_media
from app.utils.helpers.user_helpers import is_username_exist, is_email_exist
from app.utils.helpers.auth_helpers import send_code_to_email, generate_six_digit_code
from app.utils.response import error_response, success_response

class ProfileController:
    @staticmethod
    def get_profile():
        error = False
        
        try:
            current_user_id = get_jwt_identity()
            user_info = get_user_info(current_user_id)
            extra_data = {'user_profile': user_info}
        except Exception as e:
            error = True
            msg = f'An error occurred while getting user profile: {e}'
            # Log the error details for debugging
            logging.exception("An exception occurred while getting user profile.")
            status_code = 500
        
        if error:
            return error_response(msg, status_code)
        else:
            return success_response('User profile fetched successfully', 200, extra_data)



    @staticmethod
    def update_profile():
        try:
            data = request.form.to_dict()
            current_user_id = data.get('user_id', 0)
            
            console_log('current_user_id', current_user_id)
            
            current_user = User.query.get(current_user_id)
            
            console_log('current_user', current_user)
            if not current_user:
                return error_response(f"user not found", 404)
            
            user_address = current_user.address
            user_profile = current_user.profile
            user_nextofkin = current_user.nextofkin
            user_identification = current_user.identification
            # user_wallet = current_user.wallet
            
            # if not user_wallet:
                # user_wallet = Wallet.create_wallet(trendit3_user=current_user)
            
            
            console_log('content_type', request.content_type)
            
            # Get the request data
            data = request.form.to_dict()
            
            email = data.get('email', user_profile.email if user_profile else '')
            username = data.get('username', user_profile.username if user_profile else '')
            # password = data.get('password', user_profile.password if user_profile else '')
            country = data.get('country', user_profile.country if user_profile else '')
            address = data.get('address', user_profile.address if user_profile else '')
            state = data.get('state', user_profile.state if user_profile else '')
            city = data.get('city', user_profile.city if user_profile else '')
            currency_code = data.get('currency_code', user_profile.currency_code if user_profile else '')
            postal_code = data.get('postal_code', user_profile.postal_code if user_profile else '')
            firstname = data.get('firstname', user_profile.firstname if user_profile else '')
            lastname = data.get('lastname', user_profile.lastname if user_profile else '')
            gender = data.get('gender', user_profile.gender if user_profile else '')
            phone = data.get('phone', user_profile.phone if user_profile else '')
            birthday = data.get('birthday', user_profile.birthday if user_profile else '')
            profile_picture = data.get('profile_picture_id', user_profile.profile_picture if user_profile else '')
            id_type = data.get('id_type', user_profile.id_type if user_profile else '')
            id_issue_date = data.get('id_issue_date', user_profile.id_issue_date if user_profile else '')
            id_expiration_date = data.get('id_expiration_date', user_profile.id_expiration_date if user_profile else '')
            id_picture = data.get('id_picture', user_profile.id_picture if user_profile else '')
            # bvn = data.get('bvn', user_profile.bvn if user_profile else '')
            next_of_kin_firstname = data.get('next_of_kin_name', user_profile.next_of_kin_name if user_profile else '')
            next_of_kin_lastname = data.get('next_of_kin_lastname', user_profile.next_of_kin_lastname if user_profile else '')
            next_of_kin_relationship = data.get('next_of_kin_relationship', user_profile.next_of_kin_relationship if user_profile else '')
            next_of_kin_gender = data.get('next_of_kin_gender', user_profile.next_of_kin_gender if user_profile else '')
            next_of_kin_phone = data.get('next_of_kin_phone', user_profile.next_of_kin_phone if user_profile else '')
            next_of_kin_email = data.get('next_of_kin_email', user_profile.next_of_kin_email if user_profile else '')
            next_of_kin_address = data.get('next_of_kin_address', user_profile.next_of_kin_address if user_profile else '')




            console_log('profile_picture', profile_picture)
            
            
            # currency_info = {}
            # if country != user_address.country:
            #     currency_info = get_currency_info(country)
                
            #     if currency_info is None:
            #         return error_response('Error getting the currency of user\'s country', 500)
            
            
            if is_username_exist(username, current_user):
                return error_response('Username already Taken', 409)
            
            
            if isinstance(profile_picture, FileStorage) and profile_picture.filename != '':
                try:
                    profile_picture_id = save_media(profile_picture) # This saves image file, saves the path in db and return the id of the image
                except Exception as e:
                    current_app.logger.error(f"An error occurred while profile image: {str(e)}")
                    return error_response(f"An error occurred saving profile image: {str(e)}", 400)
            elif profile_picture == '' and current_user:
                if user_profile.profile_picture_id:
                    profile_picture_id = user_profile.profile_picture_id
                else:
                    profile_picture_id = None
            else:
                profile_picture_id = None
            
            # update user details
            current_user.update(username=username)
            user_profile.update(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                profile_picture_id=profile_picture_id,
                birthday=birthday,
                currency_code=currency_code,
                phone=phone,
            )

            user_nextofkin.update(
                firstname=next_of_kin_firstname,
                lastname=next_of_kin_lastname,
                relationship=next_of_kin_relationship,
                gender=next_of_kin_gender,
                phone=next_of_kin_phone,
                email=next_of_kin_email,
                address=next_of_kin_address
            )

            user_identification.update(
                id_type=id_type,
                issue_date=id_issue_date,
                expiration_date=id_expiration_date,
                id_picture=id_picture
            )

            user_address.update(
                country=country,
                state=state,
                address=address,
                city=city,
                postal_code=postal_code
            )

            # user_wallet.update(currency_name=currency_info.get('name', user_wallet.currency_name), currency_code=currency_info.get('code', user_wallet.currency_code))
                        
            
            extra_data={'user_data': current_user.to_dict()}
            api_response = success_response('User profile updated successfully', 200, extra_data)
            
        except (DataError, DatabaseError) as e:
            db.session.rollback()
            log_exception('Database error occurred during registration', e)
            api_response = error_response('Error connecting to the database.', 500)
        except Exception as e:
            db.session.rollback()
            log_exception('An exception occurred updating user profile.', e)
            api_response = error_response('An error occurred while updating user profile', 500)
        finally:
            db.session.close()
        
        return api_response
    

    @staticmethod
    def user_email_edit():
        error = False
        
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            data = request.get_json()
            new_email = data.get('new_email')
            
            if new_email == current_user.email:
                return error_response("email provided isn't a new email", 406)
            
            if is_email_exist(new_email, current_user):
                return error_response("Email already Taken", 409)
                
            verification_code = generate_six_digit_code() # Generate a random six-digit number
            
            try:
                send_code_to_email(new_email, verification_code) # send verification code to user's email
            except Exception as e:
                return error_response(f'An error occurred while sending the verification email: {str(e)}', 500)
            
            # Create a JWT that includes the user's info and the verification code
            expires = timedelta(minutes=30)
            edit_email_token = create_access_token(identity={
                'new_email': new_email,
                'user_id': get_jwt_identity(),
                'verification_code': verification_code
            }, expires_delta=expires)
        except Exception as e:
            error = True
            msg = f'An error occurred trying to change the email: {e}'
            status_code = 500
            # Log the error details for debugging
            logging.exception("An exception occurred changing the email.")
        
        if error:
            return jsonify({
                    'status': 'failed',
                    'status_code': status_code,
                    'message': msg
                }), status_code
        else:
            return jsonify({
                    'status': 'success',
                    'status_code': 200,
                    'message': 'Verification code sent successfully',
                    'edit_email_token': edit_email_token,
                }), 200


    @staticmethod
    def verify_email_edit():
        error = False
        try:
            data = request.get_json()
            edit_email_token = data.get('edit_email_token')
            entered_code = data.get('entered_code')
            
            # Decode the JWT and extract the user's info and the verification code
            decoded_token = decode_token(edit_email_token)
            user_info = decoded_token['sub']
            new_email = user_info['new_email']
            
            current_user = User.query.get(get_jwt_identity())
            
            if int(entered_code) == int(user_info['verification_code']):
                current_user.email = new_email
                db.session.commit()
                
            else:
                error = True
                msg = 'Verification code is incorrect'
                status_code = 400
        except Exception as e:
            error = True
            msg = f'An error occurred while changing your email.'
            status_code = 500
            logging.exception("An exception occurred changing your email.")
            db.session.rollback()
        finally:
            db.session.close()
        if error:
            return error_response(msg, status_code)
        else:
            return success_response('Email updated successfully', 201, {'user_email': current_user.email})


    @staticmethod
    def get_profile_pic():
        error = False
        
        try:
            current_user_id = get_jwt_identity()
            user_info = get_user_info(current_user_id)
            extra_data = {
                'profile_pic': user_info.get('profile_picture', '')
            }
        except Exception as e:
            error = True
            msg = f'An error occurred while getting profile pic: {e}'
            # Log the error details for debugging
            logging.exception("An exception occurred while getting user's profile pic.")
            status_code = 500
        
        if error:
            return error_response(msg, status_code)
        else:
            return success_response("profile pic fetched successfully", 200, extra_data)


    @staticmethod
    def update_profile_pic():
        error = False
        
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.filter(User.id == current_user_id).first()
            
            if not current_user:
                return error_response("user not found", 404)
            
            user_profile = current_user.profile
            profile_picture = request.files['profile_picture']
            
            if profile_picture.filename != '':
                try:
                    profile_picture_id = save_media(profile_picture) # This saves image file, saves the path in db and return the id of the image
                except Exception as e:
                    current_app.logger.error(f"An error occurred while saving profile image: {str(e)}")
                    return error_response(f"An error occurred saving profile image: {str(e)}", 400)
            elif profile_picture.filename == '' and current_user:
                if user_profile.profile_picture_id:
                    profile_picture_id = user_profile.profile_picture_id
                else:
                    profile_picture_id = None
            else:
                profile_picture_id = None
            
            user_profile.update(profile_picture_id=profile_picture_id)
            extra_data = {'profile_picture': user_profile.get_profile_img()}
        except Exception as e:
            error = True
            msg = f'An error occurred updating profile pic: {e}'
            status_code = 500
            logging.exception("An exception occurred while updating user's profile pic.")
            db.session.rollback()
        
        if error:
            return error_response(msg, status_code)
        else:
            return success_response("profile pic updated successfully", 200, extra_data)

    
    # @staticmethod
    # def bank_details():
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.filter(User.id == current_user_id).first()
            
            if not current_user:
                return error_response("user not found", 404)
            
            primary_bank = BankAccount.query.filter_by(trendit3_user_id=current_user_id, is_primary=True).first()
            msg = "Bank details Fetched successfully" if primary_bank else "Bank details haven't been provided"
            
            if request.method == 'POST':
                # Get the request data
                data = request.get_json()
                
                bank_name = data.get('bank_name', '')
                account_no = data.get('account_no', '')
                account_name = data.get('account_name', '')
                bank_code = get_bank_code(bank_name)
                
                if primary_bank:
                    primary_bank.update(bank_name=bank_name, bank_code=bank_code, account_no=account_no, account_name=account_name)
                else:
                    primary_bank = BankAccount.add_bank(trendit3_user=current_user, bank_name=bank_name, bank_code=bank_code, account_no=account_no, account_name=account_name, is_primary=True)
                
                msg = "Bank details updated successfully"
                extra_data = {'bank_details': primary_bank.to_dict()}
            
            extra_data = {'bank_details': primary_bank.to_dict()  if primary_bank else None}
            api_response = success_response(msg, 200, extra_data)
        except (DataError, DatabaseError) as e:
            if request.method == 'POST':
                db.session.rollback()
            log_exception('Database error occurred during registration', e)
            api_response = error_response('Error interacting to the database.', 500)
        except Exception as e:
            if request.method == 'POST':
                db.session.rollback()
            log_exception('An error occurred during registration', e)
            api_response = error_response(f'An unexpected error occurred processing the request: {str(e)}', 500)
        finally:
            db.session.close()
        
        return api_response

