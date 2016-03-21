# python imports
import os
# flask imports
from flask.ext.script import Manager, Shell
# project imports
from application import create_app
from application.database import manager as database_manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("database", database_manager)

if __name__ == '__main__':
    manager.run()
