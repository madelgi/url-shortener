import json


from url_shortener.api import users
from url_shortener.models import User, RevokedToken, UrlRegistry
from url_shortener.extensions import db

from url_shortener.util.string_encoder import base64_decode, base64_encode


def test_encode(app):
    with app.test_client() as client:
        url = "https://google.com"
        response = encode_url(client, url)
        response = json.loads(response.data.decode())
        assert response["success"]
        assert response["url"] == url
        assert response["encoding"] == base64_encode(1).decode("utf-8")

        query = db.session.query(UrlRegistry).first()
        assert query.url == "https://google.com"
        assert query.date_added
        assert not query.premium


def test_decode(app):
    with app.test_client() as client:
        url = "https://google.com"
        response = encode_url(client, url)
        encoded_url = json.loads(response.data.decode())['encoding']
        decode_response = decode_url(client, encoded_url)
        assert decode_response.status_code == 302
        assert url in decode_response.data.decode()


####################################################################################################
# Helper functions
####################################################################################################
def encode_url(client, url, jwt=None):
    headers = {}
    if jwt:
        headers = {"Authorization": f"Bearer {jwt}"}

    return client.post(
        '/encode',
        data=json.dumps(dict(
            url=url
        )),
        content_type='application/json',
        headers=headers
    )


def decode_url(client, encoded_url):
    return client.post(
        f'/{encoded_url}'
    )
