# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class DefaultConfig(object):
    DEBUG = True
    DEPLOYMENT = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'developers@abrio.ir'
    SITE_NAME = 'http://abrio.ir'

    # Blueprint need to be installed entered here
    INSTALLED_CONTROLLERS = (
        'main',
    )


class DevelopmentConfig(DefaultConfig):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
