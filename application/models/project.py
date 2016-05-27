from application.extensions import db
from uuid import uuid4
from datetime import datetime


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    private_key = db.Column(db.String(100))
    create_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'))

    @classmethod
    def generate_fake(cls, user):
        fake = Project(name="Fake Project", owner_id=user.id, private_key=str(uuid4()), create_date=datetime.utcnow())
        db.session.add(fake)
        db.session.commit()
        return fake

    def __repr__(self):
        return '<Project %r>' % self.name


class TopProject(db.Model):
    __tablename__ = 'top_projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=100, convert_unicode=True))
    description = db.Column(db.Text(length=5000, convert_unicode=True))

    def __repr__(self):
        return '<Top Project %r>' % self.name
