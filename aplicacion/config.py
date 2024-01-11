#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Config(object):
    SECRET_KEY = 'f0faa2bed03b28e48544762d760aa169'

    DEBUG = False

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pass123@mysql/colegio_entrevista'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """
    Testing configurations
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:pass123@mysql/colegio_entrevista'
    TESTING = True

class ProductionConfig(Config):
    """
    Production configurations
    """

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
