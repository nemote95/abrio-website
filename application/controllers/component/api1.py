# python imports
import os
from itsdangerous import BadSignature
from sqlalchemy import or_, and_
# flask imports
from flask import abort, Blueprint, jsonify, request, current_app, g
from application.controllers.user.api1 import auth
from flask.ext.login import current_user, login_required
# project imports
from application.models.component import Component
from application.extensions import db

__all__ = ['api']
api = Blueprint('component.api1', __name__, url_prefix='/api/v1/component')


@api.route('/create', methods=['POST'])
@auth.login_required
def create_component():
    name = request.json['name']
    is_private = request.json['isPrivate']
    new_component = Component(name=name, owner_id=g.user.id, private=is_private)
    db.session.add(new_component)
    db.session.commit()
    return jsonify(token=new_component.generate_token()), 201


@api.route('/upload', methods=['POST'])
def upload_component():
    token = request.headers.get('private key')
    version = request.headers.get('version')
    jar_file = request.files['files']
    file_type = jar_file.filename.rsplit('.', 1)[1]

    try:
        component = Component.verify_token(token)
        component.deploy_version = version
    except BadSignature:
        return abort(401)

    if file_type in current_app.config['ALLOWED_EXTENSIONS']:
        jar_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                   'components', '%s_v%s.%s' % (str(component.id), version, file_type)))
        db.session.commit()
        return jsonify(), 200
    else:
        return abort(422)


@api.route('/edit', methods=['POST'])
def edit_component():
    cid = request.json['id']
    name = request.json['name']
    version = request.json['version']
    new_component = Component.query.get(cid)
    new_component.deploy_version = version
    new_component.name = name
    print new_component.name, new_component.deploy_version
    db.session.commit()
    return jsonify(), 201


@api.route('/search/<name>', methods=['GET'])
@login_required
def search(name):
    result = [{'cid': c.id, 'name': c.name, 'private': c.private} for c in
              Component.query.filter(and_(Component.name.contains(name),
                                          or_(Component.private == False, Component.owner_id == current_user.id))).all()]
    print result
    return jsonify({"result": result}), 200
