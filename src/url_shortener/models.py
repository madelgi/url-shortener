"""Database models for the URL shortener app.
"""
import datetime

import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from url_shortener.extensions import db, login


class User(UserMixin, db.Model):
    """Model for users in our app.

    Arguments:
        _id: Auto-incrementing primary key
        username: Username
        email: User's email address
        password_hash: User's encrypted password
    """
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password: str) -> None:
        """Set user's password hash.

        Arguments:
            password: plaintext password used to generate hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if a user's password is correct.

        Arguments:
            password: plaintext password.

        Returns:
            True if the password matches, else False.
        """
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(cls, uname: str) -> 'User':
        """Return a user object based on username.

        Arguments:
            uname: The username to search.
        """
        return cls.query.filter_by(username=uname).first()

    def __repr__(self):
        return f'<User {self.username}: {self.email}>'


class UrlRegistry(db.Model):
    """Table storing our shrunken URLs

    Arguments:
        _id: Auto-incrementing primary key.
        url: Url to shrink.
        date_added: Timestamp
        premium: Whether the URL was added by a registered user
    """
    _id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    premium = db.Column(db.Boolean, default=False)


class RevokedToken(db.Model):
    """Table storing revoked tokens.

    Arguments:
        _id: Auto-incrementing primary key.
        jti: The JWT ID.
    """
    _id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        """Add the revoked token to the database.
        """
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        """Check if JWT ID is blacklisted.

        Arguments:
            jti: JWT ID to check.
        """
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
