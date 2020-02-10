import logging
import os


logger = logging.getLogger(__name__)


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'testKey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'testJWTKey')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class ProductionConfig(Config):
    username, password, db = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@postgres:5432/{db}"
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    username, password, db = os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), os.getenv('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@postgres:5432/{db}"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///url_shortener_test.db"


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
