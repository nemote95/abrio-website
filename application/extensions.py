# flask imports
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

__all__ = ["db", "login"]

db = SQLAlchemy()
login = LoginManager()
login.session_protection = 'strong'
