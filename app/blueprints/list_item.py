from typing import Optional
from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import jwt_required, get_current_user

from app.client import image_client
from app.extensions import db
from app.models import List, ListItem, User

blueprint = Blueprint('list_item', __name__)


@blueprint.route('/lists/<int:list_id>/items', methods=['GET'])
@jwt_required()
def index(list_id: int):
    current_user: User = get_current_user()
    existing_list: Optional[List] = db.session.get(List, list_id)

    if existing_list is None or existing_list.has_user(current_user) is False:
        abort(404, description=f'List by id: {list_id} not found')

    list_items = (ListItem
                  .query
                  .join(User.lists)
                  .join(List.list_items)
                  .filter(ListItem.list == existing_list)
                  .all())

    return jsonify(list_items)


@blueprint.route('/lists/<int:list_id>/items', methods=['POST'])
@jwt_required()
def store(list_id: int):
    current_user: User = get_current_user()
    existing_list: Optional[List] = db.session.get(List, list_id)

    if existing_list is None or existing_list.has_user(current_user) is False:
        abort(404, description=f'List by id: {list_id} not found')

    content = request.json
    name: str = content['name']
    icon: str = content['icon']

    existing_item_list: Optional[ListItem] = ListItem.query.filter(ListItem.name == name).first()

    if existing_item_list is not None:
        return jsonify(existing_item_list), 201

    new_item_list = ListItem(name=name, icon=icon, list=existing_list)
    db.session.add(new_item_list)
    db.session.commit()

    return jsonify(new_item_list), 201


@blueprint.route('/lists/<int:list_id>/items/<int:item_id>/upload', methods=['POST'])
@jwt_required()
def upload(list_id: int, item_id: int):
    current_user: User = get_current_user()
    existing_list: Optional[List] = db.session.get(List, list_id)

    if existing_list is None or existing_list.has_user(current_user) is False:
        abort(404, description=f'List by id: {list_id} not found')

    existing_item: Optional[ListItem] = db.session.get(ListItem, item_id)

    if existing_item is None:
        abort(404, description=f'List by id: {list_id} not found')

    if 'file' not in request.files:
        abort(400, description='Empty file')

    file = request.files['file']

    if file.filename == '':
        abort(400, description='Empty file')

    name = image_client.upload(file)

    return jsonify(url=name), 200

