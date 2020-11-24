import os

class Config(object):
    DEBUG  = False
    TESTING  =  False

class ProductionConfig(Config):
    SECRET_KEY = os.environ['SECRET_KEY']

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ['SECRET_KEY']

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ['SECRET_KEY']
