# -*- coding: utf-8 -*-

from config import DefaultConfig
from flask import Flask, render_template


def configure_app(app, configuration=DefaultConfig):
    app.config.from_object(configuration)


def configure_controllers(app):
    app.template_folder = 'templates'
    controllers = app.config['INSTALLED_CONTROLLERS']
    for controller in controllers:
        bp = __import__('application.controllers.%s' % controller, fromlist=[controller])

        for route in bp.__all__:
            route_obj = getattr(bp, route)
            app.register_blueprint(route_obj)


def configure_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(_):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(_):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(_):
        return render_template('errors/500.html'), 500


def create_app(config_name):
    app = Flask(__name__)
    configure_app(app)
    configure_controllers(app)
    configure_error_handlers(app)
    return app
