from application.extensions import db
from uuid import uuid4

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    private_key = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plans.id'))

    @classmethod
    def generate_fake(cls, user):
        fake = Project(name="Fake Project", owner_id=user.id,private_key=str(uuid4()))
        db.session.add(fake)
        db.session.commit()
        return fake

    def __repr__(self):
        return '<Project %r>' % self.name
