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
from app.models import User, Stock, RealEstate, Business, Crypto, NFT, SocialMedia
from app.utils.helpers.auth_helpers import generate_six_digit_code, save_pwd_reset_token, send_2fa_code
from app.utils.helpers.email_helpers import send_code_to_email, send_other_emails
from app.utils.helpers.basic_helpers import log_exception, console_log
from app.utils.helpers.user_helpers import get_vasset_user, is_email_exist, is_user_exist
from app.utils.helpers.media_helpers import save_media
from app.utils.response import error_response, success_response



class AssetsController:

    @staticmethod
    def add_stock():
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            symbol = data.get('symbol')
            quantity = data.get('quantity')
            new_stock = Stock(symbol=symbol, quantity=quantity, user_id=user_id)
            db.session.add(new_stock)
            db.session.commit()
            return jsonify({'message': 'Stock added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def get_stocks():
        user_id = get_jwt_identity()
        stocks = Stock.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': stock.id, 'symbol': stock.symbol, 'quantity': stock.quantity} for stock in stocks])
    
    @staticmethod
    def add_real_estate():
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            address = data.get('address')
            value = data.get('value')
            new_real_estate = RealEstate(address=address, value=value, user_id=user_id)
            db.session.add(new_real_estate)
            db.session.commit()
            return jsonify({'message': 'Real estate added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def get_real_estates():
        user_id = get_jwt_identity()
        real_estates = RealEstate.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': real_estate.id, 'address': real_estate.address, 'value': real_estate.value} for real_estate in real_estates])
    
    @staticmethod
    def add_business():
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            name = data.get('name')
            description = data.get('description', '')
            new_business = Business(name=name, description=description, user_id=user_id)
            db.session.add(new_business)
            db.session.commit()
            return jsonify({'message': 'Business added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def get_businesses():
        user_id = get_jwt_identity()
        businesses = Business.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': business.id, 'name': business.name, 'description': business.description} for business in businesses])
    
    @staticmethod
    def add_crypto():
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            new_crypto = Crypto(symbol=data['symbol'], amount=data['amount'], user_id=user_id)
            db.session.add(new_crypto)
            db.session.commit()
            return jsonify({'message': 'Crypto added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def get_cryptos():
        user_id = get_jwt_identity()
        cryptos = Crypto.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': crypto.id, 'symbol': crypto.symbol, 'amount': crypto.amount} for crypto in cryptos])
    
    @staticmethod
    def add_nft():
        user_id = get_jwt_identity()
        data = request.get_json()
        print(data)
        try:
            name = data.get('name')
            uri = data.get('uri')
            new_nft = NFT(name=name, uri=uri, user_id=user_id)
            db.session.add(new_nft)
            db.session.commit()
            return jsonify({'message': 'NFT added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    @staticmethod
    def get_nfts():
        user_id = get_jwt_identity()
        nfts = NFT.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': nft.id, 'name': nft.name, 'uri': nft.uri} for nft in nfts])


    @staticmethod
    def add_social_media():
        user_id = get_jwt_identity()
        data = request.get_json()
        try:
            platform = data.get('platform')
            username = data.get('username')
            password = data.get('password')
            description = data.get('description', '')
            new_socialmedia = SocialMedia(platform=platform, username=username, user_id=user_id, password=password, description=description)

            db.session.add(new_socialmedia)
            db.session.commit()
            return jsonify({'message': 'Social media added successfully'}), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
        
    
    @staticmethod
    def get_social_media():
        user_id = get_jwt_identity()
        socialmedia = SocialMedia.query.filter_by(user_id=user_id).all()
        return jsonify([{'id': social.id, 'platform': social.platform, 'username': social.username} for social in socialmedia])
    

    @staticmethod
    def get_all_assets():
        user_id = get_jwt_identity()
        stocks = Stock.query.filter_by(user_id=user_id).all()
        real_estates = RealEstate.query.filter_by(user_id=user_id).all()
        businesses = Business.query.filter_by(user_id=user_id).all()
        cryptos = Crypto.query.filter_by(user_id=user_id).all()
        nfts = NFT.query.filter_by(user_id=user_id).all()
        socialmedia = SocialMedia.query.filter_by(user_id=user_id).all()

        return jsonify({
            'stocks': [{'id': stock.id, 'symbol': stock.symbol, 'quantity': stock.quantity} for stock in stocks],
            'real_estates': [{'id': real_estate.id, 'address': real_estate.address, 'value': real_estate.value} for real_estate in real_estates],
            'businesses': [{'id': business.id, 'name': business.name, 'description': business.description} for business in businesses],
            'cryptos': [{'id': crypto.id, 'symbol': crypto.symbol, 'amount': crypto.amount} for crypto in cryptos],
            'nfts': [{'id': nft.id, 'name': nft.name, 'uri': nft.uri} for nft in nfts],
            'social_media': [{'id': social.id, 'platform': social.platform, 'username': social.username} for social in socialmedia]
        })