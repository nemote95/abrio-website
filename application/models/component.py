from application.extensions import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature
from flask import current_app

class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deploy_version = db.Column(db.String)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            return 401
        component = Component.query.get(data['id'])
        return component

    def __repr__(self):
        return '<Component %r>' % self.name

