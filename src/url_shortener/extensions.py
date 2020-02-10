from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login = LoginManager()
migrate = Migrate()
jwt_manager = JWTManager()
