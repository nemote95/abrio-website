from models.component import Component
from models.logic import Logic
from models.project import Project
from models.user import User
from application.extensions import db, redis

PROJECT_TEST_TOKEN = '123456'
PROJECT_CHAT_TOKEN = '123123'
PROJECT_AUTH_TOKEN = '481516'


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
    from random import randint
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

    # ---------- test project -----------
    project = Project()
    project.name = 'test'
    project.owner = user
    project.owner_id = user.id

    db.session.add(project)
    db.session.commit()
    redis.setnx('abr:' + PROJECT_TEST_TOKEN, project.id)

    component1 = Component()
    component1.name = 'First Component'
    component1.deploy_version = str(randint(0, 10))
    component1.owner_id = user.id

    db.session.add(component1)
    db.session.commit()

    component2 = Component()
    component2.name = 'Second Component'
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

    # ---------- chat project -----------
    project2 = Project()
    project2.name = 'chat'
    project2.owner = user
    project2.owner_id = user.id

    db.session.add(project2)
    db.session.commit()
    redis.setnx('abr:' + PROJECT_CHAT_TOKEN, project2.id)

    component3 = Component()
    component3.name = 'Chat component'
    component3.deploy_version = str(randint(0, 10))
    component3.owner_id = user.id

    db.session.add(component3)
    db.session.commit()

    logic4 = Logic()
    logic4.project_id = project2.id
    logic4.component_1_id = None
    logic4.component_2_id = component3.id
    logic4.message_type = 'BasicEvent'

    db.session.add(logic4)
    db.session.commit()

    logic5 = Logic()
    logic5.project_id = project2.id
    logic5.component_1_id = component3.id
    logic5.component_2_id = None
    logic5.message_type = 'BasicEvent'

    db.session.add(logic5)
    db.session.commit()

    # ---------- authentication project -----------
    project3 = Project()
    project3.name = 'auth'
    project3.owner = user

    db.session.add(project3)
    db.session.commit()
    redis.setnx('abr:' + PROJECT_AUTH_TOKEN, project3.id)

    component4 = Component()
    component4.name = 'Auth component'
    component4.deploy_version = str(randint(0, 10))
    component4.owner = user

    db.session.add(component4)
    db.session.commit()

    logic6 = Logic()
    logic6.project_id = project3.id
    logic6.component_1_id = None
    logic6.component_2_id = component4.id
    logic6.message_type = 'BasicEvent'

    db.session.add(logic6)
    db.session.commit()

    logic7 = Logic()
    logic7.project_id = project3.id
    logic7.component_1_id = component4.id
    logic7.component_2_id = None
    logic7.message_type = 'BasicEvent'

    db.session.add(logic7)
    db.session.commit()
