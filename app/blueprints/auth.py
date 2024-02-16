from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from app.models import User

blueprint = Blueprint('auth', __name__)


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()

    if not user or not check_password_hash(user.password, password):
        abort(401, 'Bad username or password')

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)
