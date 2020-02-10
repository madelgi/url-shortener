import pytest


from url_shortener.models import (
    User,
    UrlRegistry,
    RevokedToken
)

user = User(username='luis', email='luis@gmail.com')
user.set_password('pass123')
url = UrlRegistry(url='https://google.com')


def test_user_initialization():
    assert user.email == 'luis@gmail.com'
    assert user.username == 'luis'


def test_user_password():
    assert user.check_password('pass123')
    assert user.password_hash is not None
    assert user.password_hash != 'pass123'


def test_user_find_by_username():
    assert False, "Not implemented"


def test_url_registry_initialization():
    assert url.url == 'https://google.com'
    print(url.date_added)
    assert url.date_added is not None
    assert not url.premium
