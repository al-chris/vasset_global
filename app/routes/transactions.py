'''
Note: All routes require JWT authentication.

Author:
    Chris
Link:
    https://github.com/al-chris
Package:
    VASSET
'''
from flask_jwt_extended import jwt_required

from . import api
from app.views import TransactionController

@api.route('/payment', methods=['POST'])
@jwt_required()
def make_payment():
    return TransactionController.make_payment()

@api.route('/payment/screenshot/<int:transaction_id>', methods=['POST'])
@jwt_required()
def upload_screenshot(transaction_id):
    return TransactionController.upload_screenshot(transaction_id=transaction_id)

@api.route('/payment/verify/<int:transaction_id>', methods=['POST'])
@jwt_required()
def verify_payment(transaction_id):
    return TransactionController.verify_payment(transaction_id=transaction_id)

@api.route('/payment/cancel/<int:transaction_id>', methods=['POST'])
@jwt_required()
def cancel_payment(transaction_id):
    return TransactionController.cancel_payment(transaction_id=transaction_id)

@api.route('/user/<int:user_id>/transactions', methods=['GET'])
@jwt_required()
def get_transactions(user_id):
    return TransactionController.get_transactions(user_id=user_id)