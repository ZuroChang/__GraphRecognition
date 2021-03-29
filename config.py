# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 14:58:17 2020

@author: ZuroChang
"""


import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='Test'
    MAIL_SERVER=''
    MAIL_PORT=0
    MAIL_USE_TLS=''
    MAIL_USERNAME=''
    MAIL_PASSWORD=''
    FLASKY_MAIL_SUBJECT_PREFIX='[Flasky]'
    FLASKY_MAIL_SENDER=''
    FLASKY_ADMIN=''
    SQLACHEMY_TRACK_MODIFICATIONS=False
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=''
    
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI=''
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=''

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    
    'default':DevelopmentConfig
}


