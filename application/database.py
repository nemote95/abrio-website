# flask imports
from flask.ext.script import Manager, prompt_bool
# project imports
from application.extensions import db

manager = Manager(usage="Perform database operations")


@manager.command
def drop():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def create():
    """Creates database tables from SqlAlchemy models"""
    db.create_all()


@manager.command
def recreate():
    """
    Recreates database tables (same as issuing 'drop' and then 'create')
    """
    drop()
    create()
