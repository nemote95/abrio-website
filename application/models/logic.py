from application.extensions import db


class Logic(db.Model):
    __tablename__ = 'Logic'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    component_1_id = db.Column(db.Integer, db.ForeignKey('components.id'))
    component_2_id = db.Column(db.Integer, db.ForeignKey('components.id'))
    message_type = db.Column(db.Enum('BasicEvent', 'type_b'))

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
            self.project_id, self.component_id1, self.component_id2, self.message_type)
