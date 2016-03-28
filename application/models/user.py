from application.extensions import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def generate_fake(cls):
        from faker import Factory
        faker = Factory.create()
        fake = User(
            email=faker.email(),
            password='123123',
            name=faker.name(),
            company=faker.company(),
            phone_number=faker.phone_number(),
            ssn=faker.profile()["ssn"]
        )

        db.session.add(fake)
        db.session.commit()
        return fake

    def __repr__(self):
        return '<User %r>' % self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
