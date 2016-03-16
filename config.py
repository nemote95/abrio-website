# python imports
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = True
    DEPLOYMENT = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'developers@abrio.ir'

    TEMPLATE = ''
    SITE_NAME = 'Abrio'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Blueprint need to be installed entered here
    INSTALLED_CONTROLLERS = (
        'main',
        'user'
    )


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
