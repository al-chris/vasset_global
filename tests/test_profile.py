import pytest
from app import db
from app.models import User
from flask_jwt_extended import create_access_token


@pytest.fixture(scope='module')
def new_user():
    user = User(
        email="test@example.com",
        username="testuser",
        password="testpassword"
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='module')
def auth_headers(test_client, new_user):
    access_token = create_access_token(identity=new_user.id)
    return {
        'Authorization': f'Bearer {access_token}'
    }


def test_get_profile(test_client, auth_headers):
    response = test_client.get('/api/profile', headers=auth_headers)
    assert response.status_code == 200
    assert 'User profile fetched successfully' in str(response.data)


def test_update_profile(test_client, auth_headers, new_user):
    update_data = {
        "user_id": new_user.id,
        "firstname": "Updated",
        "lastname": "User",
        "phone": "08098765432"
    }
    response = test_client.post('/api/profile/update', headers=auth_headers, data=update_data)
    assert response.status_code == 200
    assert 'User profile updated successfully' in str(response.data)


def test_get_profile_pic(test_client, auth_headers):
    response = test_client.get('/api/profile-pic', headers=auth_headers)
    assert response.status_code == 200
    assert 'profile pic fetched successfully' in str(response.data)


def test_update_profile_pic(test_client, auth_headers):
    with open('test_image.jpg', 'rb') as img:
        response = test_client.post('/api/profile-pic/edit', headers=auth_headers, data={'profile_picture': img})
    assert response.status_code == 200
    assert 'profile pic updated successfully' in str(response.data)
