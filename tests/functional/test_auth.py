def test_successful_login_endpoint(app_test_client):
    response = app_test_client.post('/login', json={'username': 'test', 'password': 'testing'})
    assert response.status_code == 200


def test_bad_login_endpoint(app_test_client):
    response = app_test_client.post('/login', json={'username': '213', 'password': '123'})
    assert response.status_code == 401
