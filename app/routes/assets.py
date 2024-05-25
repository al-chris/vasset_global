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