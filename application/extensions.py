# flask imports
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from application.email import MailGunEmail
from flask.ext.admin import Admin
from application.flaskadmin import AdminIndexView

__all__ = ["db", "login_manager", "kvsession", "redis", "email", "admin"]

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'

redis = redis.StrictRedis()
kvsession = KVSessionExtension(RedisStore(redis))

email = MailGunEmail()

admin = Admin(template_mode='bootstrap3', index_view=AdminIndexView())
