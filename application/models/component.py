import os
from application.extensions import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
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

    @classmethod
    def verify_token(cls, token):
        """
        :raises BadSignature
        :param token:
        :return: component object that match token
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        data = s.loads(token)
        component = cls.query.get(data['id'])
        return component

    def component_files(self):
        directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'components')
        return [filename for filename in os.listdir(directory) if filename.startswith(str(self.id))]

    def __repr__(self):
        return '<Component %r>' % self.name
