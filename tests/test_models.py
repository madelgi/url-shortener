import pytest


from url_shortener.models import (
    UrlRegistry,
    RevokedToken
)

url = UrlRegistry(url='https://google.com')


def test_user_initialization(new_user):
    assert new_user.email == 'luis@gmail.com'
    assert new_user.username == 'luis'


def test_user_password(new_user):
    assert new_user.check_password('pass123')
    assert new_user.password_hash is not None
    assert new_user.password_hash != 'pass123'


def test_url_registry_initialization():
    assert url.url == 'https://google.com'
    assert not url.premium
