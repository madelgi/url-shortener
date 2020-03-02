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
from url_shortener.models import UrlRegistry, Users

logger = logging.getLogger(__name__)

urls_bp = Blueprint('shorten', __name__)
urls = flask_restful.Api(urls_bp)


# Set expiry to one week
EXPIRY_PERIOD = 60 * 60 * 24 * 7


class Decode(Resource):
    def get(self, encoded_str:  str):
        """Use encoded string to  fetch URL from the URL registry.

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

        # If associated with registered user, we don't delete the URL. Otherwise, expire after 7 days.
        if not q.user_id and (q.date_added + timedelta(seconds=EXPIRY_PERIOD)) < datetime.now():
            db.session.query(UrlRegistry).filter(UrlRegistry._id == decoded).delete()
            db.session.commit()
            return {"success": False, "message": "Url has expired. Deleting record."}, 498

        return redirect(q.url)


class Encode(Resource):
    """Resource for creating and managing encoded URLs.
    """
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        parser.add_argument('encoded_str', type=str)
        self.parser = parser

    @jwt_optional
    def post(self) -> (dict, int):
        """Encode a URL.

        Arguments:
            url: The URL to encode.
        """
        args = self.parser.parse_args()
        url = str(args['url'])

        db_obj = UrlRegistry(url=url)

        # Check if user passes JWT
        user_id = get_raw_jwt().get('identity')
        user = Users.find_by_username(user_id)
        if user:
            db_obj.user_id = user._id

        db.session.add(db_obj)
        db.session.commit()
        return_obj = {
            "success": True,
            "url": url,
            "encoding": se.base64_encode(db_obj._id).decode("utf-8")
        }
        return return_obj, 200

    def get(self) -> (dict, int):
        """Get an existing encoded URL.

        Arguments:
            encoded_str: The string representing the encoded URL.
        """
        encoded_str = str(self.parser.parse_args()['encoded_str'])
        decoded = se.base64_decode(encoded_str)
        q = db.session.query(UrlRegistry).filter(UrlRegistry._id == decoded).first()

        if not q:
            return {"success": False, "message": f"String {encoded_str} does not map to an URL."}, 404

        expiry = None
        if not q.user_id:
            expiry = q.date_added + timedelta(seconds=EXPIRY_PERIOD)

        return {"success": True, "url": q.url, "expiry": str(expiry)}, 200

    def put(self) -> (dict, int):
        """Update an existing URL.

        Arguments:
            encoded_str: Base64-encoded string mapping to the existing URL.
            url: Url to replace the existing URL.
        """
        args = self.parser.parse_args()
        encoded_str, new_url = str(args['encoded_str']), str(args['url'])
        decoded = se.base64_decode(encoded_str)
        q = db.session.query(UrlRegistry).filter(UrlRegistry._id == decoded).first()

        if not q:
            return {"success": False, "message": f"String {encoded_str} does not map to an URL."}, 404

        old_url, q.url = q.url, new_url
        db.session.commit()
        return {"success": True, "old_url": old_url, "new_url": new_url}, 200


urls.add_resource(Encode, '/encode')
urls.add_resource(Decode, '/<string:encoded_str>')
