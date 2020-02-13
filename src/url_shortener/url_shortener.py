from flask import Flask

from werkzeug.exceptions import HTTPException, BadRequest
from sqlalchemy.exc import IntegrityError

from url_shortener.config import config_by_name


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    from .extensions import db, flask_bcrypt, login, migrate, jwt_manager
    db.init_app(app)
    migrate.init_app(app, db=db)
    flask_bcrypt.init_app(app)
    login.init_app(app)
    jwt_manager.init_app(app)
    from .api.users import users, users_bp
    from .api.urls import urls, urls_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(urls_bp)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app: Flask):
    from .errors import handle_http_exception, handle_value_error
    app.register_error_handler(BadRequest, handle_http_exception)
    app.register_error_handler(ValueError, handle_value_error)
