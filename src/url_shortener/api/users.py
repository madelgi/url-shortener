import logging

import flask_restful
from flask_restful import Resource, reqparse
from flask import Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    jwt_optional
)

from url_shortener.extensions import db, jwt_manager
from url_shortener.models import User, RevokedToken

logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__)
users = flask_restful.Api(users_bp)


class Register(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        self.parser = parser

    def post(self):
        args = self.parser.parse_args()
        username, email, password = str(args['username']), str(args['email']), str(args['password'])
        if User.find_by_username(username):
            return {"success": False, "message": f"User {username} already exists"}

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return {
            "success": True,
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class Login(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        self.parser = parser

    def post(self):
        args = self.parser.parse_args()
        username, password = str(args['username']), str(args['password'])
        current_user = User.find_by_username(username)
        if not current_user:
            return {"success": False, "message": f"User '{username}' does not exist"}

        if not current_user.check_password(password):
            return {"success": False, "message": "Incorrect password"}

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return {
            "success": True,
            'access_token': access_token,
            'refresh_token': refresh_token
        }


class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedToken(jti=jti)
        revoked_token.add()
        return {"success": True}


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_token = RevokedToken(jti=jti)
        revoked_token.add()
        return {"success": True}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"success": True, "access_token": access_token}


class Secret(Resource):
    @jwt_optional
    def get(self):
        jwt = get_raw_jwt()
        return {"message": "secret", "jwt": jwt}


@jwt_manager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


users.add_resource(Register, '/registration')
users.add_resource(Login, '/login')
users.add_resource(LogoutAccess, '/logout/access')
users.add_resource(LogoutRefresh, '/logout/refresh')
users.add_resource(TokenRefresh, '/token/refresh')
users.add_resource(Secret, '/secret')
