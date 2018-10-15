import os


class Config:
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):

    DEBUG = True
    TESTING = False


class TestingConfig(Config):

    DEBUG = True
    TESTING = True
    DB_NAME = os.getenv('DB_TEST_NAME')


class ProductionConfig(Config):
    pass


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
