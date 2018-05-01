from .default import Config


class ProductionConfig(Config):
    # App config

    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

