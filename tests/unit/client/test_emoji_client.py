import json
from app.client.emoji_client import search_emoji


def test_emoji_client(requests_mock):
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

    result = search_emoji('value')
    assert result == '🛌🏿'
