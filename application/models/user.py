from application.extensions import db, login_manager
from enums import Abilities
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from sqlalchemy import and_
from sqlalchemy import UniqueConstraint


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    ssn = db.Column(db.String(10))

    projects = db.relationship('Project', backref='users',
                               lazy='dynamic', cascade='all,delete')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=7 * 24 * 60 * 60):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    @classmethod
    def generate_fake(cls):
        from faker import Factory
        faker = Factory.create()
        fake = User()
        fake.email = faker.email()
        fake.password = '123123'
        fake.name = faker.name()
        fake.company = faker.company()
        fake.phone_number = faker.phone_number()
        fake.ssn = faker.profile()["ssn"]

        db.session.add(fake)
        db.session.commit()
        return fake

    def has_ability(self, ability):
        user_abilities = UserAbility.query.with_entities(UserAbility.aid).filter_by(uid=self.id).all()
        return (ability,) in user_abilities or (Abilities.ALL,) in user_abilities

    def is_admin(self):
        return self.has_ability(Abilities.ALL)


    def add_ability(self, ability):
        user_ability = UserAbility(aid=ability, uid=self.id)
        db.session.add(user_ability)
        db.session.commit()

    def remove_ability(self, ability):
        user_ability = UserAbility.query.filter_by(
            and_(UserAbility.uid == self.id, UserAbility.aid == ability)).one_or_none()
        if user_ability:
            db.session.delete(user_ability)
            db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserAbility(db.Model, UserMixin):
    __tablename__ = 'user_ability'
    id = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (
        UniqueConstraint("aid", "uid"),
    )
