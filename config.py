import os
from datetime import timedelta


# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = "dev"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BCRYPT_LOG_ROUNDS = 15
    WTF_CSRF_ENABLED = True
    REMEMBER_COOKIE_DURATION = timedelta(days=14)


class ProductionConfig(Config):
    FLASK_ENV = "prod"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}",
    )
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
