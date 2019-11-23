import os

class Config:
    '''
    general configuration
    '''
    SQLALCHEMY_DATABASE_URI = 'postgres://hzdjuymgaykvle:4079958f7180f18102b516a8f427e0794e8f22080047c631e44d39f929359d5a@ec2-54-235-240-126.compute-1.amazonaws.com:5432/di59qlb6lan20'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    '''
    production configuration child class
    '''

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    '''
    development configuration child class
    '''
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

config_options = {
    'development': DevConfig,
    'production': ProdConfig
}