# tests/test_auth.py

import pytest
import json
from app import create_app, db
from app.models import User, UserSettings, OneTimeToken
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
        user_setting = UserSettings(vasset_user=user)
        otp = OneTimeToken(vasset_user=user)
        db.session.add_all([user, user_setting, otp])
        db.session.commit()


def test_signup(client):
    data = {
        'email': 'newuser@example.com',
        'username': 'newuser',
        'password': 'newpassword'
    }
    response = client.post(url_for('api.signUp'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b'Registration completed successfully' in response.data


def test_signup_existing_email(client, init_db):
    data = {
        'email': 'testuser@example.com',
        'username': 'anotheruser',
        'password': 'anotherpassword'
    }
    response = client.post(url_for('api.signUp'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 409
    assert b'Email already taken' in response.data


def test_signup_existing_username(client, init_db):
    data = {
        'email': 'anotheruser@example.com',
        'username': 'testuser',
        'password': 'anotherpassword'
    }
    response = client.post(url_for('api.signUp'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 409
    assert b'Username already taken' in response.data


def test_login(client, init_db):
    data = {
        'email_username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post(url_for('api.login'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data


def test_login_wrong_password(client, init_db):
    data = {
        'email_username': 'testuser',
        'password': 'wrongpassword'
    }
    response = client.post(url_for('api.login'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401
    assert b'Password is incorrect' in response.data


def test_username_check(client):
    response = client.get(url_for('api.username_check'), data=json.dumps({'username': 'testuser'}), content_type='application/json')
    assert response.status_code == 409
    assert b'testuser is already Taken' in response.data


def test_username_check_available(client):
    response = client.get(url_for('api.username_check'), data=json.dumps({'username': 'newusername'}), content_type='application/json')
    assert response.status_code == 200
    assert b'newusername is available' in response.data


def test_email_check(client):
    response = client.get(url_for('api.email_check'), data=json.dumps({'email': 'testuser@example.com'}), content_type='application/json')
    assert response.status_code == 409
    assert b'testuser@example.com is already taken' in response.data


def test_email_check_available(client):
    response = client.get(url_for('api.email_check'), data=json.dumps({'email': 'newuser@example.com'}), content_type='application/json')
    assert response.status_code == 200
    assert b'newuser@example.com is available' in response.data


def test_logout(client, init_db):
    user = User.query.first()
    access_token = create_access_token(identity=user.id)
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.delete(url_for('api.logout'), headers=headers)
    assert response.status_code == 200
    assert b'User logged out successfully' in response.data


def test_forgot_password(client, init_db):
    data = {'email_username': 'testuser'}
    response = client.post(url_for('api.forgot_password'), data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b'Password reset code sent successfully' in response.data


def test_reset_password(client, init_db):
    user = User.query.first()
    reset_token = create_access_token(identity={
        'username': user.username,
        'email': user.email,
        'reset_code': '123456'
    }, expires_delta=False)

    data = {
        'reset_token': reset_token,
        'entered_code': '123456',
        'new_password': 'newpassword'
    }
    response = client.post('api.reset_password', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert b'Password changed successfully' in response.data
