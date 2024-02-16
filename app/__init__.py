from dotenv import dotenv_values
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(dotenv_values())

    from app.extensions import db, jwt
    db.init_app(app)
    jwt.init_app(app)

    from app.blueprints import list, list_item, grocery, auth
    app.register_blueprint(list.blueprint)
    app.register_blueprint(list_item.blueprint)
    app.register_blueprint(grocery.blueprint)
    app.register_blueprint(auth.blueprint)

    with app.app_context():
        db.create_all()

    @app.errorhandler(400)
    def resource_bad_request(e):
        return jsonify(error=str(e)), 400

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(401)
    def resource_unauthorized(e):
        return jsonify(error=str(e)), 401

    return app
