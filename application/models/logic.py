from application.extensions import db
from sqlalchemy import UniqueConstraint


class Logic(db.Model):
    __tablename__ = 'logic'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    component_1_id = db.Column(db.Integer, db.ForeignKey('components.id'))
    component_2_id = db.Column(db.Integer, db.ForeignKey('components.id'))
    message_type = db.Column(db.Enum('BasicEvent',
                                     'RequestEvent',
                                     'Response',
                                     'NewEvent',
                                     'type_b', name='message_type'))
    __table_args__ = (
        UniqueConstraint("project_id", "component_1_id", "component_2_id", "message_type"),
    )

    @classmethod
    def generate_fake(cls, project, component1, component2):
        from random import randint
        message_type = Logic.message_type.property.columns[0].type.enums[randint(0, 1)]
        fake = Logic(project_id=project.id, component_1_id=component1.id, component_2_id=component2.id,
                     message_type=message_type)
        db.session.add(fake)
        db.session.commit()
        return fake

    def __repr__(self):
        return '<Logic project:%d component.No1:%d component.No2:%d message type:%r>' % (
            self.project_id, self.component_1_id, self.component_2_id, self.message_type)
