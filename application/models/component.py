from application.extensions import db


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Component %r>' % self.name

