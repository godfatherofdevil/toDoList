class Config:
    """ Base config class. Inherit and over-write for required configurations """

    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {"db": "todo", "host": "localhost", "port": 27017}


class DevConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {"db": "todo", "host": "localhost", "port": 27017}


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        "db": "mongoenginetest",
        "host": "mongomock://localhost",
        "port": 27017,
    }


class ProdConfig(Config):
    pass


app_config = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
