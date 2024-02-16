from conftest import app_test_client
from app.models import List


def test_cannot_access_lists_endpoint(app_test_client):
    response = app_test_client.get('/lists')
    assert response.status_code == 401


def test_lists_endpoint(app_auth_test_client):
    response = app_auth_test_client.get('/lists')
    assert response.status_code == 200
    assert len(response.json) == 1


def test_create_endpoint(app_auth_test_client):
    response = app_auth_test_client.post('/lists', json={'name': 'Another Test List'})
    assert response.status_code == 201
    assert response.json['name'] == 'Another Test List'
    with app_auth_test_client.application.app_context():
        count = List.query.count()
        assert count == 2


def test_validate_create_endpoint(app_auth_test_client):
    response = app_auth_test_client.post('/lists', json={'name': 'Test List'})
    assert response.status_code == 400
    assert response.json['error'] == '400 Bad Request: List by name Test List already exists'
    with app_auth_test_client.application.app_context():
        count = List.query.count()
        assert count == 1
