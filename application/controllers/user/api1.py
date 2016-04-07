# flask imports
from flask import g
from flask.ext.httpauth import HTTPBasicAuth
# project imports
from application.models.user import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    new_user = User.query.filter_by(email=email).one_or_none()
    if not new_user or not new_user.verify_password(password):
        return False
    g.user = new_user
    return True
