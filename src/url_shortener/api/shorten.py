"""Logic for URL encoding.
"""
import logging
from datetime import timedelta, datetime

import flask_restful
from flask_restful import Resource, reqparse
from flask import Blueprint, redirect, jsonify
from flask_jwt_extended import jwt_optional, get_raw_jwt

import url_shortener.util.string_encoder as se
from url_shortener.extensions import db
from url_shortener.models import UrlRegistry, User

logger = logging.getLogger(__name__)

shorten_bp = Blueprint('shorten', __name__)
shorten = flask_restful.Api(shorten_bp)


# Set expiry to one week
EXPIRY_PERIOD = 60 * 60 * 24 * 7


class Decode(Resource):
    def post(self, encoded_str: str):
        """Use encoded string to fetch URL from the URL registry.

        Arguments:
            encoded_str: Base64 encoded string, corresponding to an id in the URL registry.

        Returns:
            A redirect to the decoded URL. The URL is deleted if it has reached its expiry
            date.
        """
        decoded = se.base64_decode(encoded_str)
        q = db.session.query(UrlRegistry).filter(UrlRegistry._id == decoded).first()

        if not q:
            return {"success": False, "message": f"String {encoded_str} does not map to an URL."}, 404

        if not q.premium and (q.date_added + timedelta(seconds=EXPIRY_PERIOD)) < datetime.now():
            db.session.query(UrlRegistry).filter(UrlRegistry._id == decoded).delete()
            db.session.commit()
            return {"success": False, "message": "Url has expired. Deleting record."}, 498

        return redirect(q.url)


class Encode(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        self.parser = parser

    @jwt_optional
    def post(self) -> str:
        """Encode a URL.

        Arguments:
            url: The URL to encode.
        """
        args = self.parser.parse_args()
        url = str(args['url'])

        db_obj = UrlRegistry(url=url)

        # Check if user passes JWT
        user_id = get_raw_jwt().get('identity')
        if user_id and User.find_by_username(user_id):
            db_obj.premium = True

        db.session.add(db_obj)
        db.session.commit()
        return_obj = {
            "success": True,
            "url": url,
            "encoding": se.base64_encode(db_obj._id).decode("utf-8")
        }
        return return_obj, 200


shorten.add_resource(Encode, '/encode')
shorten.add_resource(Decode, '/<string:encoded_str>')
