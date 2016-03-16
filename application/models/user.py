from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask.ext.login import UserMixin
from application.extensions import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    company = db.Column(db.String(64))
    phone_number= db.Column(db.String(15))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
