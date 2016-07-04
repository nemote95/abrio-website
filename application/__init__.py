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

    @app.errorhandler(401)
    def page_not_found(_):
        return render_template('errors/401.html'), 401

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
    components_path = os.path.join(app.config['COMPONENT_UPLOAD_FOLDER'])
    if not os.path.exists(components_path):
        os.makedirs(components_path)


def configure_admin(app):
    from application.extensions import db, admin, redis
    from application.flaskadmin import AdminIndexView, AdminRedis, AdminModelView, AdminFile, AdminTopProjectView, \
        AdminComponentView, AdminProjectView
    from application.models.user import User, UserAbility
    from application.models.component import Component
    from application.models.project import Project, TopProject
    from application.models.logic import Logic
    admin.add_view(AdminModelView(User, session=db.session, name='Users', endpoint='admin.user', url='/admin/user'))
    admin.add_view(AdminModelView(UserAbility, session=db.session, name='UserAbilities', endpoint='admin.user-ability',
                                  url='/admin/user_ability'))
    admin.add_view(AdminComponentView(Component, session=db.session, name='Components', endpoint='admin.component',
                                      url='/admin/component'))
    admin.add_view(
        AdminProjectView(Project, session=db.session, name='Projects', endpoint='admin.project', url='/admin/project'))
    admin.add_view(AdminTopProjectView(TopProject, session=db.session, name='TopProjects', endpoint='admin.top-project',
                                       url='/admin/top_project'))
    admin.add_view(AdminModelView(Logic, session=db.session, name='Logics', endpoint='admin.logic', url='/admin/logic'))
    admin.add_view(AdminRedis(redis, category='Tools', endpoint='admin.redis', url='/admin/redis'))
    admin.add_view(AdminFile(app.config['UPLOAD_FOLDER'], endpoint="admin.upload", url='/upload/', name='UploadFiles'))
    admin.add_view(
        AdminFile(app.config['SDK_DIRECTORY'], endpoint="admin.sdk", url='/sdk_files/', name='DownloadSDKFiles'))


def create_app(config_name):
    app = Flask(__name__)
    configure_app(app)
    configure_extensions(app)
    configure_controllers(app)
    configure_APIs(app)
    configure_error_handlers(app)
    configure_upload_directories(app)
    configure_admin(app)
    return app
