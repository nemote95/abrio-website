# python imports
import os
# flask imports
from flask import Flask, render_template
# project imports
from config import DefaultConfig


def configure_app(app, configuration=DefaultConfig):
    app.config.from_object(configuration)
    app.config.from_pyfile('environ.py', silent=True)


def configure_extensions(app):
    import application.extensions as ex

    for extension in ex.__all__:
        try:
            getattr(ex, extension).init_app(app)
        except (AttributeError, TypeError):
            pass


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


def configure_controllers(app):
    controllers = app.config['INSTALLED_CONTROLLERS']
    for controller in controllers:
        if controller == 'main':
            bp = __import__('application.controllers.%s' % controller, fromlist=[controller])
        else:
            bp = __import__('application.controllers.%s.web' % controller, fromlist=['.web'])

        for route in bp.__all__:
            route_obj = getattr(bp, route)
            app.register_blueprint(route_obj)


def configure_APIs(app):
    apis = app.config['INSTALLED_API']
    version = app.config['API_VERSION']
    for api in apis:
        bp = __import__('application.controllers.%s.api%s' % (api, version), fromlist=[api])

        for route in bp.__all__:
            route_obj = getattr(bp, route)
            app.register_blueprint(route_obj)


def configure_upload_directories(app):
    for dir in app.config['UPLOAD_DIRECTORIES']:
        path = os.path.join(app.config['UPLOAD_FOLDER'], dir)
        if not os.path.exists(path):
            os.makedirs(path)


def create_app(config_name):
    app = Flask(__name__)
    configure_app(app)
    configure_controllers(app)
    configure_APIs(app)
    configure_extensions(app)
    configure_error_handlers(app)
    configure_upload_directories(app)
    return app
