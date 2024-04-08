import pytest
from dotenv import load_dotenv, find_dotenv, dotenv_values
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
import app
from app.extensions import db
from app.models import List, User, ListItem


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv(find_dotenv('.env.test'))


@pytest.fixture()
def app_test():
    test_app = app.create_app()
    test_app.config['TESTING'] = True
    test_app.config['DEBUG'] = True

    with test_app.app_context():
        db.create_all()
        load_data()

    yield test_app

    with test_app.app_context():
        db.drop_all()


@pytest.fixture
def app_test_client(app_test):
    client = app_test.test_client()

    yield client


@pytest.fixture
def app_auth_test_client(app_test):
    with app_test.app_context():
        existing_user: User = User.query.first()
        access_token = create_access_token(existing_user)

    client = app_test.test_client()
    client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

    yield client


def load_data():
    test_list = List(name='Test List')
    test_item = ListItem(name='Milk', icon='🥛', list=test_list)
    test_user = User(username='test', password=generate_password_hash('testing', 'pbkdf2'))
    test_user.add_list(test_list)
    db.session.add_all([test_user, test_list, test_item])
    db.session.commit()
