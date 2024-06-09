'''
This module defines the controller methods for transaction operations in the Vasset Global Flask application.

It includes methods for checking username, checking email, signing up, resending email verification code, and logging in.

@author: Chris
@link: https://github.com/al-chris
@package: VASSET
'''

import logging
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from sqlalchemy.exc import (IntegrityError, DataError, DatabaseError, InvalidRequestError)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.datastructures import FileStorage
from flask_jwt_extended import create_access_token, decode_token, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt import ExpiredSignatureError, DecodeError
import pyotp

from app.extensions import db
from app.models import User, Stock, RealEstate, Business, Crypto, NFT, SocialMedia, Transactions
from app.utils.helpers.auth_helpers import generate_six_digit_code, save_pwd_reset_token, send_2fa_code
from app.utils.helpers.email_helpers import send_code_to_email, send_other_emails
from app.utils.helpers.basic_helpers import log_exception, console_log
from app.utils.helpers.user_helpers import get_vasset_user, is_email_exist, is_user_exist
from app.utils.helpers.media_helpers import save_media
from app.utils.response import error_response, success_response

import cloudinary
import cloudinary.uploader
from config import Config

cloudinary.config( 
    cloud_name = Config.CLOUDINARY_CLOUD_NAME, 
    api_key = Config.CLOUDINARY_API_KEY, 
    api_secret = Config.CLOUDINARY_API_SECRET 
)


class TransactionController:
    
    @staticmethod
    def make_payment():
        """
        Create a new payment transaction.
        
        Expects JSON data with 'user_id', 'amount', and 'wallet_address'.
        
        - 'user_id': ID of the user making the payment.
        - 'amount': Amount of the transaction.
        - 'wallet_address': Crypto wallet address to which the payment is made.
        
        Returns:
            - 201: Transaction created successfully with transaction ID.
            - 404: User not found.
            - 400: Bad request or database error.
        """
        data = request.json
        # user_id = data.get('user_id', 0)
        user_id = get_jwt_identity()
        amount = int(data.get('amount'))
        wallet_address = data.get('wallet_address')
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        try:
            transaction = Transactions(
                amount=amount,
                wallet_address=wallet_address,
                user_id=user_id
            )
            db.session.add(transaction)
            db.session.commit()
            return jsonify({'message': 'Transaction created', 'transaction_id': transaction.id}), 201
        except (IntegrityError, DataError, DatabaseError, InvalidRequestError) as e:
            db.session.rollback()
            return jsonify({'message': 'Database error', 'error': str(e)}), 400

    @staticmethod
    def upload_screenshot(transaction_id):
        """
        Upload a screenshot of the transaction for verification.
        
        Expects a file upload with 'screenshot' as the key.
        
        - 'transaction_id': ID of the transaction to upload the screenshot for.
        
        Returns:
            - 200: Screenshot uploaded successfully with the URL.
            - 400: No file uploaded or database error.
            - 404: Transaction not found.
        """
        transaction = Transactions.query.get(transaction_id)
        if not transaction:
            return jsonify({'message': 'Transaction not found'}), 404
        
        file = request.files['screenshot']
        if file:
            try:
                result = cloudinary.uploader.upload(file)
                transaction.screenshot_url = result['secure_url']
                db.session.commit()
                return jsonify({'message': 'Screenshot uploaded', 'url': transaction.screenshot_url}), 200
            except (IntegrityError, DataError, DatabaseError, InvalidRequestError) as e:
                db.session.rollback()
                return jsonify({'message': 'Database error', 'error': str(e)}), 400
        return jsonify({'message': 'No file uploaded'}), 400
    
    @staticmethod
    def verify_payment(transaction_id):
        """
        Verify a payment transaction and update the user's balance.
        
        - 'transaction_id': ID of the transaction to verify.
        
        Returns:
            - 200: Transaction verified and balance updated.
            - 404: Transaction not found.
            - 400: Database error.
            - 401: Unauthorized.
        """
        user_id = int(get_jwt_identity())
        if user_id != Config.ADMIN_ID:
            return jsonify({'message': 'Unauthorized'}), 401
        
        transaction = Transactions.query.get(transaction_id)
        if not transaction:
            return jsonify({'message': 'Transaction not found'}), 404
        
        try:
            transaction.status = 'verified'
            transaction.user.balance += transaction.amount
            db.session.commit()
            return jsonify({'message': 'Transaction verified and balance updated'}), 200
        except (IntegrityError, DataError, DatabaseError, InvalidRequestError) as e:
            db.session.rollback()
            return jsonify({'message': 'Database error', 'error': str(e)}), 400

    @staticmethod
    def cancel_payment(transaction_id):
        """
        Cancel a pending payment transaction.
        
        Expects JSON data with 'user_id'.
        
        - 'transaction_id': ID of the transaction to cancel.
        
        Returns:
            - 200: Transaction cancelled successfully.
            - 400: Only pending transactions can be cancelled or database error.
            - 403: Only the user who created the transaction can cancel it.
            - 404: Transaction not found.
        """

        # user_id = request.json.get('user_id', 0)
        user_id = get_jwt_identity()
        transaction = Transactions.query.get(transaction_id)
        
        if not transaction:
            return jsonify({'message': 'Transaction not found'}), 404
        
        if transaction.user_id != user_id:
            return jsonify({'message': 'You can only cancel your own transactions'}), 403
        
        if transaction.status != 'pending':
            return jsonify({'message': 'Only pending transactions can be cancelled'}), 400
        
        try:
            transaction.status = 'cancelled'
            db.session.commit()
            return jsonify({'message': 'Transaction cancelled'}), 200
        except (IntegrityError, DataError, DatabaseError, InvalidRequestError) as e:
            db.session.rollback()
            return jsonify({'message': 'Database error', 'error': str(e)}), 400

    @staticmethod
    def get_transactions(user_id):
        """
        Get a list of all transactions for a user.
        
        - 'user_id': ID of the user to retrieve transactions for.
        
        Returns:
            - 200: List of transactions.
            - 404: User not found.
            - 400: Database error.
        """
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        try:
            transactions = Transactions.query.filter_by(user_id=user_id).all()
            transactions_list = [{
                'id': t.id,
                'amount': t.amount,
                'wallet_address': t.wallet_address,
                'screenshot_url': t.screenshot_url,
                'status': t.status
            } for t in transactions]
            
            return jsonify(transactions_list), 200
        except (IntegrityError, DataError, DatabaseError, InvalidRequestError) as e:
            return jsonify({'message': 'Database error', 'error': str(e)}), 400