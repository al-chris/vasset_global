# tests/test_profile.py

import pytest
import json
import io
from app import create_app, db
from app.models import User, Profile, Address
from flask import url_for
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        # Create initial data for tests
        user = User(email='testuser@example.com', username='testuser', password='testpassword')
        profile = Profile(vasset_user=user)
        address = Address(vasset_user=user)
        db.session.add_all([user, profile, address])
        db.session.commit()  # Ensure the data is committed


def get_auth_headers(user):
    access_token = create_access_token(identity=user.id)
    return {'Authorization': f'Bearer {access_token}'}

def test_get_profile(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    response = client.get(url_for('api.get_user_profile'), headers=headers)
    assert response.status_code == 200
    assert b'User profile fetched successfully' in response.data

def test_update_user_profile(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    data = {
        'vasset_user_id': user.id,
        'firstname': 'UpdatedFirstName',
        'lastname': 'UpdatedLastName',
        'gender': 'Male',
        'birthday': '1990-01-01',
        'currency_code': 'USD',
        'phone': '1234567890',
        'profile_picture_id': ''
    }
    response = client.post(url_for('api.update_user_profile'), data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    assert b'User profile updated successfully' in response.data

def test_update_nextofkin(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    data = {
        'vasset_user_id': user.id,
        'next_of_kin_firstname': 'KinFirstName',
        'next_of_kin_lastname': 'KinLastName',
        'next_of_kin_relationship': 'Sibling',
        'next_of_kin_gender': 'Female',
        'next_of_kin_phone': '0987654321',
        'next_of_kin_email': 'kin@example.com',
        'next_of_kin_address': '123 Kin Street'
    }
    response = client.post(url_for('api.update_nextofkin'), data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    assert b'Next of kin updated successfully' in response.data

def test_update_identification(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    data = {
        'vasset_user_id': user.id,
        'id_type': 'Passport',
        'id_issue_date': '2020-01-01',
        'id_expiration_date': '2030-01-01',
        'id_picture': ''
    }
    response = client.post('/api//profile/update-identification', data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    assert b'Identification updated successfully' in response.data

def test_update_address(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    data = {
        'vasset_user_id': user.id,
        'country': 'USA',
        'state': 'California',
        'address': '123 Main Street',
        'city': 'Los Angeles',
        'postal_code': '90001'
    }
    response = client.post('/api/profile/update-address', data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    assert b'Address updated successfully' in response.data

def test_get_profile_pic(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    response = client.get(url_for('api.get_profile_pic'), headers=headers)
    assert response.status_code == 200
    assert b'profile pic fetched successfully' in response.data

def test_update_profile_pic(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    data = {
        'profile_picture': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    response = client.post(url_for('api.update_profile_pic'), data=data, content_type='multipart/form-data', headers=headers)
    assert response.status_code == 200
    assert b'profile pic updated successfully' in response.data

def test_user_email_edit(client, init_db):
    user = User.query.first()
    headers = get_auth_headers(user)
    data = {
        'new_email': 'newemail@example.com'
    }
    response = client.post(url_for('api.user_email_edit'), data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 200
    assert b'Verification code sent successfully' in response.data

def test_verify_email_edit(client, init_db):
    user = User.query.first()
    new_email = 'newemail@example.com'
    verification_code = '123456'
    edit_email_token = create_access_token(identity={
        'new_email': new_email,
        'vasset_user_id': user.id,
        'verification_code': verification_code
    }, expires_delta=False)

    headers = get_auth_headers(user)
    data = {
        'edit_email_token': edit_email_token,
        'entered_code': verification_code
    }
    response = client.post(url_for('api.verify_email_edit'), data=json.dumps(data), content_type='application/json', headers=headers)
    assert response.status_code == 201
    assert b'Email updated successfully' in response.data
