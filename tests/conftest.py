#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for url_shortener.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

import pytest
from url_shortener.models import (
    User,
)
from url_shortener.config import TestingConfig
from url_shortener.url_shortener import create_app
from url_shortener.extensions import db


@pytest.fixture
def app():
    app = create_app('test')
    app.config.from_object(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def new_user():
    user = User(username='luis', email='luis@gmail.com')
    user.set_password('pass123')
    return user
