from flask import Blueprint, jsonify, request, abort

from app.exceptions import ClientException
from app.models import Grocery
from app.extensions import db
from app.client.emoji_client import search_emoji

blueprint = Blueprint('grocery', __name__)


@blueprint.route('/search', methods=['GET'])
def search():
    name = request.args.get('name', '')
    groceries = Grocery.query.filter(Grocery.name.like(f'%{name}%')).all()

    if not groceries:
        try:
            emoji = search_emoji(name)

            new_grocery = Grocery(name=name, icon=emoji)
            db.session.add(new_grocery)
            db.session.commit()
        except ClientException:
            abort(404, 'Not found')

        groceries.append(new_grocery)

    return jsonify(groceries)
