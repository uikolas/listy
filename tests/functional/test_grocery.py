import json

from conftest import app_test_client
from app.extensions import db
from app.models import Grocery


def test_food_search_endpoint(app_test_client):
    with app_test_client.application.app_context():
        new_food = Grocery(name='Salad', icon='🥗')
        db.session.add(new_food)
        db.session.commit()

    response = app_test_client.get('/search?name=ad')
    assert response.status_code == 200
    assert len(response.json) == 1


def test_use_emoji_client_if_empty_response(app_test_client, requests_mock):
    mock_json_response = """
    [
        {
            "slug": "e4-0-person-in-bed-dark-skin-tone",
            "character": "🛌🏿",
            "unicodeName": "E4.0 person in bed: dark skin tone"
        },
        {
            "slug": "e0-7-bed",
            "character": "🛏️",
            "unicodeName": "E0.7 bed"
        }
    ]
    """

    requests_mock.get(
        'https://emoji-api.com/emojis?search=value&access_key=key',
        json=json.loads(mock_json_response),
        status_code=200
    )

    response = app_test_client.get('/search?name=value')
    assert response.status_code == 200
    assert len(response.json) == 1
    with app_test_client.application.app_context():
        existing_grocery: Grocery = Grocery.query.first()
        assert existing_grocery.name == 'value'
        assert existing_grocery.icon == '🛌🏿'


def test_return_not_found(app_test_client, requests_mock):
    mock_json_response = """
    {
        "status": "error",
        "message": "No results found"
    }
    """

    requests_mock.get(
        'https://emoji-api.com/emojis?search=value&access_key=key',
        json=json.loads(mock_json_response),
        status_code=200
    )

    response = app_test_client.get('/search?name=value')
    assert response.status_code == 404
    with app_test_client.application.app_context():
        existing_grocery: Grocery = Grocery.query.first()
        assert existing_grocery is None
