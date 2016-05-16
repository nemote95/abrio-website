# flask imports
from flask import g, request, jsonify,Blueprint
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.login import current_user, login_required
# project imports
from application.extensions import db
from application.models.user import User

__all__ = ['api']
auth = HTTPBasicAuth()
api = Blueprint('user.api1', __name__, url_prefix='/api/v1/user')

@auth.verify_password
def verify_password(email, password):
    new_user = User.query.filter_by(email=email).one_or_none()
    if not new_user or not new_user.verify_password(password):
        return False
    g.user = new_user
    return True


@api.route('/edit', methods=['Post'])
@login_required
def edit_profile():
    u = User.query.filter_by(id=current_user.id).one()
    if request.json['company']:
        u.company = request.json['company']
    if request.json['name']:
        u.name = request.json['name']
    if request.json['phone_number']:
        u.phone_number = request.json['phone_number']
    if request.json['ssn']:
        u.ssn = request.json['ssn']
    db.session.commit()
    return jsonify(), 200
