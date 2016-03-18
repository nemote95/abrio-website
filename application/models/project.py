from application.extensions import db


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    file_path = db.Column(db.String())
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    git_url = db.Column(db.String())

    def __repr__(self):
        return '<Project %r>' % self.name

