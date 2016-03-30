# flask imports
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from application.email import MailGunEmail

__all__ = ["db", "login_manager", "kvsession", "redis","email"]

db = SQLAlchemy()

login_manager = LoginManager()

login_manager.session_protection = 'strong'
redis = redis.StrictRedis()
kvsession = KVSessionExtension(RedisStore(redis))

email = MailGunEmail()
