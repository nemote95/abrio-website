from models.component import Component
from models.user import User
from models.project import Project
from models.logic import Logic


def generate_fake():
    user = User.query.filter_by(id=1).one()
    component1 = Component.generate_fake(user)
    component2 = Component.generate_fake(user)
    project = Project.generate_fake(user)
    Logic.generate_fake(project, component1, component2)