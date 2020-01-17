import os


class Config:
    """ Base config class. Inherit and over-write for required configurations """
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        "db": "todo",
        "host": "localhost",
        "port": 27017
    }


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True


class ProdConfig(Config):
    pass


app_config = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}

