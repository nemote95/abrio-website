import os
from application.extensions import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class Component(db.Model):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    deploy_version = db.Column(db.String(16))
    private = db.Column(db.Boolean, default=True)
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
        directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'components')
        return [filename for filename in os.listdir(directory) if filename.startswith(str(self.id))]

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
        for i in range(int(fake.deploy_version)):
            copyfile(current_app.config['FAKE_UPLOAD'], os.path.join(current_app.config['UPLOAD_FOLDER'], 'components',
                                                                     '%s_v%s.%s' % (
                                                                         str(fake.id), i, 'jar')))
        return fake

    def __repr__(self):
        return '<Component %r>' % self.name
