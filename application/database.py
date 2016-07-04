# flask imports
from flask.ext.script import Manager, prompt_bool
# project imports
from application.extensions import db, redis

manager = Manager(usage="Perform database operations")


@manager.command
def drop():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data"):
        from application.models.logic import Logic
        db.metadata.drop_all(db.engine, tables=[Logic.__table__])
        db.drop_all()
        redis.flushall()


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


@manager.command
def fake():
    from application.generate_fake import generate_fake
    generate_fake()

@manager.command
def refresh():
    """Drops database, recreates it and inserts fake data in tables and redis"""
    from application.models.logic import Logic
    db.metadata.drop_all(db.engine, tables=[Logic.__table__])
    db.drop_all()
    redis.flushall()
    create()
    fake()

