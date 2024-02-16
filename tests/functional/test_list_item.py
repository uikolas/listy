from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import List, ListItem, User


def test_list_items_endpoint(app_auth_test_client):
    with app_auth_test_client.application.app_context():
        existing_list: List = List.query.first()

    response = app_auth_test_client.get(f'/lists/{str(existing_list.id)}/items')

    assert response.status_code == 200
    assert len(response.json) == 1


def test_create_list_items_endpoint(app_auth_test_client):
    with app_auth_test_client.application.app_context():
        existing_list: List = List.query.first()

    response = app_auth_test_client.post(f'/lists/{str(existing_list.id)}/items', json={'name': 'banana', 'icon': '🍌'})

    assert response.status_code == 201
    with app_auth_test_client.application.app_context():
        existing_list: List = List.query.first()
        count = len(existing_list.list_items)
        assert count == 2


def test_return_not_found_list_items_endpoint(app_auth_test_client):
    response = app_auth_test_client.get('/lists/10001/items')
    assert response.status_code == 404
    assert response.json['error'] == '404 Not Found: List by id: 10001 not found'


def test_return_not_found_list_items_endpoint_if_access_another_user_list_items(app_auth_test_client):
    with app_auth_test_client.application.app_context():
        create_another_user()
        existing_list: List = List.query.filter(List.name == 'Another user Test List').first()

    response = app_auth_test_client.get(f'/lists/{str(existing_list.id)}/items')

    assert response.status_code == 404
    assert response.json['error'] == f'404 Not Found: List by id: {str(existing_list.id)} not found'


def test_return_not_found_list_items_endpoint_if_access_another_user_list_items_create(app_auth_test_client):
    with app_auth_test_client.application.app_context():
        create_another_user()
        existing_list: List = List.query.filter(List.name == 'Another user Test List').first()

    response = app_auth_test_client.post(f'/lists/{str(existing_list.id)}/items', json={'name': 'banana', 'icon': '🍌'})

    assert response.status_code == 404
    assert response.json['error'] == f'404 Not Found: List by id: {str(existing_list.id)} not found'


def create_another_user():
    test_list = List(name='Another user Test List')
    test_item = ListItem(name='banana', icon='🍌', list=test_list)
    test_user = User(username='another_user', password=generate_password_hash('testing', 'pbkdf2'))
    test_user.add_list(test_list)
    db.session.add_all([test_user, test_list, test_item])
    db.session.commit()
