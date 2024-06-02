from flask import request, jsonify
from flask_jwt_extended import jwt_required

from . import api

import requests


# Replace this with the actual API endpoint you are using
CRYPTO_API_URL = 'https://api.coingecko.com/api/v3/coins/markets'
LOGO_BASE_URL = 'https://assets.coingecko.com/coins/images'

@api.route('/crypto/<crypto_id>', methods=['GET'])
def get_crypto(crypto_id):
    # Fetching cryptocurrency data
    params = {
        'vs_currency': 'usd',
        'ids': crypto_id
    }
    response = requests.get(CRYPTO_API_URL, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'Unable to fetch data from the API'}), response.status_code

    data = response.json()
    
    if not data:
        return jsonify({'error': 'Cryptocurrency not found'}), 404

    crypto_data = data[0]
    crypto_info = {
        'id': crypto_data['id'],
        'name': crypto_data['name'],
        'symbol': crypto_data['symbol'],
        'current_price': crypto_data['current_price'],
        'logo_url': f"{LOGO_BASE_URL}/{crypto_data['id']}/{crypto_data['image'].split('/')[-1]}"
    }

    return jsonify(crypto_info)


@api.route('/cryptos', methods=['GET'])
def get_cryptos():
    # Get the 'per_page' and 'page' parameters from the request
    per_page = request.args.get('per_page', 10)
    page = request.args.get('page', 1)
    
    # Fetching cryptocurrency data
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': per_page,
        'page': page,
        'sparkline': 'false'
    }
    response = requests.get(CRYPTO_API_URL, params=params)
    
    if response.status_code != 200:
        return jsonify({'error': 'Unable to fetch data from the API'}), response.status_code

    data = response.json()
    
    if not data:
        return jsonify({'error': 'No cryptocurrencies found'}), 404

    crypto_list = []
    for crypto_data in data:
        crypto_info = {
            'id': crypto_data['id'],
            'name': crypto_data['name'],
            'symbol': crypto_data['symbol'],
            'current_price': crypto_data['current_price'],
            'logo_url': crypto_data['image']
        }
        crypto_list.append(crypto_info)

    return jsonify(crypto_list)