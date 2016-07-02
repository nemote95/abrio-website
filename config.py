# python imports
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = True
    DEPLOYMENT = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'developers_sk@abrio.ir'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'developers_ps@abrio.ir'
    EXPIRATION = 7 * 24 * 60 * 60

    TEMPLATE = ''
    SITE_NAME = 'Abrio'

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Upload Configurations
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads/'
    FAKE_UPLOAD = 'fake upload/sample.jar'
    UPLOAD_DIRECTORIES = ['components', 'logos', 'top_projects']
    ALLOWED_EXTENSIONS = {'jar'}

    # Download SDK
    SDK_DIRECTORY = os.environ.get('SDK_DIRECTORY') or 'sdk/'

    # Email Configurations
    REQUEST_URL = os.environ.get('REQUEST_URL')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    NO_REPLY_MAIL_ADDRESS = os.environ.get('NO_REPLY_MAIL_ADDRESS')
    NO_REPLY_MAIL_NAME = 'Abrio No-Reply'

    # Blueprint need to be installed entered here
    INSTALLED_CONTROLLERS = (
        'main',
        'user',
        'component',
        'project',
    )

    INSTALLED_API = (
        'component',
        'project',
        'user',
    )

    API_VERSION = '1'


class DevelopmentConfig(DefaultConfig):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
