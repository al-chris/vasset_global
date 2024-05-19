import pytest
from app import db
from app.models import User
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='module')
def user_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword",
        "country": "Nigeria",
        "address": "123 Test Street",
        "state": "Lagos",
        "city": "Ikeja",
        "currency_code": "NGN",
        "postal_code": "100001",
        "firstname": "Test",
        "lastname": "User",
        "gender": "Male",
        "phone": "08012345678",
        "birthday": "1990-01-01",
        "profile_picture_id": 1,
        "id_type": "National ID",
        "id_issue_date": "2020-01-01",
        "id_expiration_date": "2030-01-01",
        "id_picture": "",
        "bvn": "12345678901",
        "next_of_kin_name": "Jane",
        "next_of_kin_lastname": "Doe",
        "next_of_kin_relationship": "Sister",
        "next_of_kin_gender": "Female",
        "next_of_kin_phone": "08098765432",
        "next_of_kin_email": "jane@example.com",
        "next_of_kin_address": "456 Test Street"
    }


def test_user_signup(test_client, user_data):
    response = test_client.post('/api/signup', json=user_data)
    assert response.status_code == 200
    assert 'Registration completed successfully' in str(response.data)


def test_user_login(test_client, user_data):
    test_client.post('/api/signup', json=user_data)
    login_data = {
        "email_username": "testuser",
        "password": "testpassword"
    }
    response = test_client.post('/api/login', json=login_data)
    assert response.status_code == 200
    assert 'Logged in successfully' in str(response.data)


def test_forgot_password(test_client, user_data):
    test_client.post('/api/signup', json=user_data)
    forgot_password_data = {
        "email_username": "testuser"
    }
    response = test_client.post('/api/forgot-password', json=forgot_password_data)
    assert response.status_code == 200
    assert 'Password reset code sent successfully' in str(response.data)


def test_reset_password(test_client, user_data):
    test_client.post('/api/signup', json=user_data)
    forgot_password_data = {
        "email_username": "testuser"
    }
    test_client.post('/api/forgot-password', json=forgot_password_data)
    
    reset_token = 'mocked_reset_token'
    reset_password_data = {
        "reset_token": reset_token,
        "entered_code": "123456",
        "new_password": "newtestpassword"
    }
    response = test_client.post('/api/reset-password', json=reset_password_data)
    assert response.status_code == 200
    assert 'Password changed successfully' in str(response.data)
