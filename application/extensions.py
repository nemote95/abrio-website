# flask imports
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import redis
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore

__all__ = ["db", "login_manager","kvsession"]

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

store = RedisStore(redis.StrictRedis())
kvsession = KVSessionExtension(store)
