from application.extensions import db


class Logic(db.Model):
    __tablename__ = 'Logic'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)
    component_id1 = db.Column(db.Integer, db.ForeignKey('components.id'), primary_key=True)
    component_id2 = db.Column(db.Integer, db.ForeignKey('components.id'), primary_key=True)
    message_type = db.Column(db.Enum('type_a', 'type_b'), primary_key=True)

    def __repr__(self):
        return '<Logic project:%d component.No1:%d component.No2:%d message type:%r>' % (
            self.project_id, self.component_id1, self.component_id2, self.message_type)
