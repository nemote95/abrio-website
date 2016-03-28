from models.component import Component
from models.user import User
from models.project import Project
from models.logic import Logic
from models.user import User


def generate_fake():
    for u in range(3):
        user = User.generate_fake()
        for p in range(2):
            project = Project.generate_fake(user)
            for c in range(5):
                component1 = Component.generate_fake(user)
                component2 = Component.generate_fake(user)
            Logic.generate_fake(project, component1, component2)