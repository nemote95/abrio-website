# -*- coding: utf-8 -*-

"""
@author: Negmo
"""

from flask import Flask, render_template
from config import DefaultConfig


def configure_app(app, configuration=DefaultConfig):
    app.config.from_object(configuration)


def configure_controllers(app):
    controllers = app.config['INSTALLED_CONTROLLERS']
    for controller in controllers:
        bp = __import__('application.controllers.%s' % controller, fromlist=[controller])

        for route in bp.__all__:
            route_obj = getattr(bp, route)
            app.register_blueprint(route_obj)


def create_app(config_name):
    app = Flask(__name__)
    configure_app(app)
    configure_controllers(app)
    return app
