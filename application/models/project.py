from application.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    plan = db.Column(db.Integer, db.ForeignKey('plans.id'))

    def __repr__(self):
        return '<Project %r>' % self.name

