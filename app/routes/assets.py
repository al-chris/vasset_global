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
    AssetsController.add_stock()

@api.route('/users/stocks', methods=['GET'])
@jwt_required()
def get_stocks():
    AssetsController.get_stocks()

# RealEstate endpoints
@api.route('/users/real_estates', methods=['POST'])
@jwt_required()
def add_real_estate():
    AssetsController.add_real_estate()

@api.route('/users/real_estates', methods=['GET'])
@jwt_required()
def get_real_estates():
    AssetsController.get_real_estates()

# Business endpoints
@api.route('/users/businesses', methods=['POST'])
@jwt_required()
def add_business():
    AssetsController.add_business()

@api.route('/users/businesses', methods=['GET'])
@jwt_required()
def get_businesses():
    AssetsController.get_businesses()

# Crypto endpoints
@api.route('/users/cryptos', methods=['POST'])
@jwt_required()
def add_crypto():
    AssetsController.add_crypto()

@api.route('/users/cryptos', methods=['GET'])
@jwt_required()
def get_cryptos():
    AssetsController.get_cryptos()

# NFT endpoints
@api.route('/users/nfts', methods=['POST'])
@jwt_required()
def add_nft():
    AssetsController.add_nft()

@api.route('/users/nfts', methods=['GET'])
@jwt_required()
def get_nfts():
    AssetsController.get_nfts()

# SocialMedia endpoints
@api.route('/users/social_media', methods=['POST'])
@jwt_required()
def add_social_media():
    AssetsController.add_social_media()


@api.route('/users/social_media', methods=['GET'])
@jwt_required()
def get_social_media():
    AssetsController.get_social_media()

# Get all assets
@api.route('/users/assets', methods=['GET'])
@jwt_required()
def get_all_assets():
    AssetsController.get_all_assets()
# app/views/assets.py