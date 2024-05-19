import pytest
from app import create_app, db
from app.models import User

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_name="testing")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()
            db.session.remove()

@pytest.fixture(scope='module')
def new_user():
    user = User(
        email="test@example.com",
        username="testuser",
        password="testpassword"
    )
    return user
