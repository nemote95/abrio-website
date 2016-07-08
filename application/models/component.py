import os
from itsdangerous import JSONWebSignatureSerializer as Serializer
from sqlalchemy import UniqueConstraint

from flask import current_app

from application.extensions import db


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    deploy_version = db.Column(db.String(16))
    private = db.Column(db.Boolean, default=True)
    mean = db.Column(db.Float(precision=1), default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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
        return [filename for filename in os.listdir(current_app.config['COMPONENT_UPLOAD_FOLDER']) if
                filename.startswith(str(self.id))]

    def to_json(self):
        return {"pid": self.id, "name": self.name, "deploy_version": self.deploy_version, "private": self.private}

    @classmethod
    def generate_fake(cls, user):
        from shutil import copyfile
        from random import randint
        fake = Component(
            name='Fake Component',
            deploy_version=randint(0, 10),
            owner_id=user.id
        )
        db.session.add(fake)
        db.session.commit()
        """apply deploy version again"""
        copyfile(current_app.config['FAKE_UPLOAD'],
                 os.path.join(current_app.config['UPLOAD_FOLDER'], 'components',
                              '%s.%s' % (str(fake.id), 'jar')))
        return fake

    def __repr__(self):
        return '<Component %r>' % self.name


class Star(db.Model):
    __tablename__ = 'stars'
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Integer, default=0)
    __table_args__ = (
        UniqueConstraint("component_id", "user_id"),
    )
