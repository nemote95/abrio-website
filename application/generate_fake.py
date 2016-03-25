from models.component import Component
from models.user import User
from models.project import Project


def generate_fake():
    user = User.query.filter_by(id=1).one()
    component1 = Component.generate_fake(user)
    component = Component.generate_fake(user)
    project = Project.generate_fake(user)