# app/routes/assets.py

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

from app.views import AssetsController




# Stock endpoints
@api.route('/users/stocks', methods=['POST'])
@jwt_required()
def add_stock():
    return AssetsController.add_stock()

@api.route('/users/stocks', methods=['GET'])
@jwt_required()
def get_stocks():
    return AssetsController.get_stocks()

# RealEstate endpoints
@api.route('/users/real_estates', methods=['POST'])
@jwt_required()
def add_real_estate():
    return AssetsController.add_real_estate()

@api.route('/users/real_estates', methods=['GET'])
@jwt_required()
def get_real_estates():
    return AssetsController.get_real_estates()

# Business endpoints
@api.route('/users/businesses', methods=['POST'])
@jwt_required()
def add_business():
    return AssetsController.add_business()

@api.route('/users/businesses', methods=['GET'])
@jwt_required()
def get_businesses():
    return AssetsController.get_businesses()

# Crypto endpoints
@api.route('/users/cryptos', methods=['POST'])
@jwt_required()
def add_crypto():
    return AssetsController.add_crypto()

@api.route('/users/cryptos', methods=['GET'])
@jwt_required()
def get_cryptos():
    return AssetsController.get_cryptos()

# NFT endpoints
@api.route('/users/nfts', methods=['POST'])
@jwt_required()
def add_nft():
    return AssetsController.add_nft()

@api.route('/users/nfts', methods=['GET'])
@jwt_required()
def get_nfts():
    return AssetsController.get_nfts()

# SocialMedia endpoints
@api.route('/users/social_media', methods=['POST'])
@jwt_required()
def add_social_media():
    return AssetsController.add_social_media()


@api.route('/users/social_media', methods=['GET'])
@jwt_required()
def get_social_media():
    return AssetsController.get_social_media()

# Youtube endpoints
@api.route('/users/youtube', methods=['POST'])
@jwt_required()
def add_youtube():
    return AssetsController.add_youtube()

@api.route('/users/youtube', methods=['GET'])
@jwt_required()
def get_youtube():
    return AssetsController.get_youtube()

# Get all assets
@api.route('/users/assets', methods=['GET'])
@jwt_required()
def get_all_assets():
    return AssetsController.get_all_assets()
# app/views/assets.py