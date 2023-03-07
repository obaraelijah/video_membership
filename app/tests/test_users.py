import pytest
from app.users.models import User
from app import db

@pytest.fixture(scope='module')
def setup():
    session = db.get_session()
    yield session
    q = User.objects.filter(email='test@gmail.com')
    if q.count() != 0:
        q.delete()
    session.shutdown()

def test_create_user(setup):
    User.create_user(email='test@gmail.com', password='abc123')

def test_duplicate_user(setup):
    with pytest.raises(Exception):
            User.create_user(email='test@gmail.com',
            password='abc12333445')


def test_invalid_email(setup):
    with pytest.raises(Exception):
            User.create_user(email='test@gmail',
            password='abc12333445')
            

def test_valid_password(setup):
    q = User.objects.filter(email='test@gmail.com')
    assert q.count() == 1
    user_obj = q.first()
    assert user_obj.verify_password('abc123') == True
    assert user_obj.verify_password('abc1243') == False