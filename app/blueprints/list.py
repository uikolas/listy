from typing import Optional
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_current_user

from app.extensions import db
from app.models import List, User

blueprint = Blueprint('list', __name__)


@blueprint.route('/lists', methods=['GET'])
@jwt_required()
def index():
    current_user: User = get_current_user()
    lists = current_user.lists

    return jsonify(lists)


@blueprint.route('/lists', methods=['POST'])
@jwt_required()
def store():
    current_user: User = get_current_user()

    content = request.json
    name: str = content['name']

    existing_list: Optional[List] = List.query.filter(List.name == name).first()

    if existing_list is not None:
        abort(400, description=f'List by name {name} already exists')

    new_list: List = List(name=name)
    current_user.add_list(new_list)

    db.session.add(new_list)
    db.session.commit()

    return jsonify(new_list), 201
