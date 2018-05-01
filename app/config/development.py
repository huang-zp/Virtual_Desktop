# coding: utf-8
from .default import Config


class DevelopmentConfig(Config):
    # App config

    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@127.0.0.1/virtual_desktop"

