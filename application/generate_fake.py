from models.component import Component
from models.logic import Logic
from models.project import Project
from models.user import User
from application.extensions import db, redis
from random import randint

PROJECT_TEST_TOKEN = '123456'
PROJECT_CHAT_TOKEN = '123123'
PROJECT_AUTH_TOKEN = '481516'
PROJECT_DISP_TOKEN = '091973'


def generate_fake():
    generate_development_data()

    for u in range(3):
        user = User.generate_fake()
        for p in range(2):
            project = Project.generate_fake(user)
            for c in range(5):
                component1 = Component.generate_fake(user)
                component2 = Component.generate_fake(user)
                Logic.generate_fake(project, component1, component2)


def generate_development_data():
    user = User()
    user.company = 'Abrio'
    user.confirmed = True
    user.email = 'az.bardia13@gmail.com'
    user.name = 'BANK_H'
    user.phone_number = '0912345689'
    user.password = '123123'
    user.ssn = '0017578167'

    db.session.add(user)
    db.session.commit()
    generate_project_multiplier_data(user)
    generate_project_chat_data(user)
    generate_project_auth_data(user)
    generate_project_dispatcher_data(user)


def generate_project_multiplier_data(user):
    project = Project()
    project.name = 'multiplier'
    project.owner = user
    project.owner_id = user.id
    project.private_key = PROJECT_TEST_TOKEN

    db.session.add(project)
    db.session.commit()
    redis.setnx('abr:' + PROJECT_TEST_TOKEN, project.id)

    component1 = Component()
    component1.name = 'multiplier 2'
    component1.deploy_version = str(randint(0, 10))
    component1.owner_id = user.id

    db.session.add(component1)
    db.session.commit()

    component2 = Component()
    component2.name = 'multiplier 3'
    component2.deploy_version = str(randint(0, 10))
    component2.owner_id = user.id

    db.session.add(component2)
    db.session.commit()

    logic1 = Logic()
    logic1.project_id = project.id
    logic1.component_1_id = component1.id
    logic1.component_2_id = component2.id
    logic1.message_type = 'BasicEvent'

    db.session.add(logic1)
    db.session.commit()

    logic2 = Logic()
    logic2.project_id = project.id
    logic2.component_1_id = None
    logic2.component_2_id = component1.id
    logic2.message_type = 'BasicEvent'

    db.session.add(logic2)
    db.session.commit()

    logic3 = Logic()
    logic3.project_id = project.id
    logic3.component_1_id = component2.id
    logic3.component_2_id = None
    logic3.message_type = 'BasicEvent'

    db.session.add(logic3)
    db.session.commit()


def generate_project_chat_data(user):
    project = Project()
    project.name = 'chat'
    project.owner = user
    project.owner_id = user.id
    project.private_key = PROJECT_CHAT_TOKEN

    db.session.add(project)
    db.session.commit()
    redis.setnx('abr:' + PROJECT_CHAT_TOKEN, project.id)

    component = Component()
    component.name = 'Chat component'
    component.deploy_version = str(randint(0, 10))
    component.owner_id = user.id

    db.session.add(component)
    db.session.commit()

    logic1 = Logic()
    logic1.project_id = project.id
    logic1.component_1_id = None
    logic1.component_2_id = component.id
    logic1.message_type = 'BasicEvent'

    db.session.add(logic1)
    db.session.commit()

    logic2 = Logic()
    logic2.project_id = project.id
    logic2.component_1_id = component.id
    logic2.component_2_id = None
    logic2.message_type = 'BasicEvent'

    db.session.add(logic2)
    db.session.commit()


def generate_project_auth_data(user):
    component = Component()
    component.name = 'auth'
    component.deploy_version = str(randint(0, 10))
    component.owner_id = user.id
    db.session.add(component)
    db.session.commit()


def generate_project_dispatcher_data(user):
    project = Project()
    project.name = 'football kaghazi'
    project.owner = user
    project.owner_id = user.id
    project.private_key = PROJECT_DISP_TOKEN

    db.session.add(project)
    db.session.commit()
    redis.setnx('abr:' + PROJECT_DISP_TOKEN, project.id)

    component = Component()
    component.name = 'One to one dispatcher'
    component.deploy_version = str(randint(0, 10))
    component.owner_id = user.id

    db.session.add(component)
    db.session.commit()

    logic1 = Logic()
    logic1.project_id = project.id
    logic1.component_1_id = None
    logic1.component_2_id = component.id
    logic1.message_type = 'BasicEvent'

    db.session.add(logic1)
    db.session.commit()

    logic2 = Logic()
    logic2.project_id = project.id
    logic2.component_1_id = component.id
    logic2.component_2_id = None
    logic2.message_type = 'BasicEvent'

    db.session.add(logic2)
    db.session.commit()
