import os

from url_shortener.config import (
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    Config
)


def test_config():
    assert Config.JWT_BLACKLIST_ENABLED
    assert Config.JWT_BLACKLIST_TOKEN_CHECKS == ['access', 'refresh']


def test_development_config():
    assert DevelopmentConfig.SQLALCHEMY_DATABASE_URI.split(':')[0] == 'postgresql'
    assert DevelopmentConfig.DEBUG
    assert not DevelopmentConfig.SQLALCHEMY_TRACK_MODIFICATIONS


def test_testing_config():
    assert TestingConfig.DEBUG
    assert TestingConfig.TESTING
    assert TestingConfig.SQLALCHEMY_DATABASE_URI.split(':')[0] == 'sqlite'
    assert not TestingConfig.SQLALCHEMY_TRACK_MODIFICATIONS


def test_production_config():
    assert ProductionConfig.SQLALCHEMY_DATABASE_URI.split(':')[0] == 'postgresql'
    assert not ProductionConfig.DEBUG
