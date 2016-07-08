# python imports
import os
from itsdangerous import BadSignature
from sqlalchemy import or_, and_
from flask import abort, Blueprint, jsonify, request, current_app, g
from application.controllers.user.api1 import auth
from flask.ext.login import current_user, login_required
from application.models.component import Component, Star
from application.models.logic import Logic
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
    """apply deploy version again"""
    if file_type in current_app.config['ALLOWED_EXTENSIONS']:
        jar_file.save(
            os.path.join(current_app.config['COMPONENT_UPLOAD_FOLDER'], '%s.%s' % (str(component.id), file_type)))
        db.session.commit()
        return jsonify(), 200
    else:
        return abort(422)


@api.route('/edit', methods=['POST'])
@login_required
def edit_component():
    print request.json
    cid = request.json['id']
    name = request.json['name']
    new_component = Component.query.get(cid)
    new_component.name = name
    """apply version"""
    # if request.json['version']:
    # new_component.deploy_version = request.json['version']
    db.session.commit()
    return jsonify(), 201


@api.route('/delete', methods=['DELETE'])
def delete():
    token = request.headers.get('private key')
    component = Component.verify_token(token)
    if component:
        if not Logic.query.filter(
                or_(Logic.component_1_id == component.id, Logic.component_2_id == component.id)).all():
            db.session.delete(component)
            db.session.commit()
            return jsonify(), 200
        else:
            return abort(403)
    else:
        return abort(401)


@api.route('/search/<name>')
@api.route('/search/')
@login_required
def search(name=""):
    components = Component.query.filter(and_(Component.name.contains(name),
                                             or_(Component.private == False,
                                                 Component.owner_id == current_user.id))).order_by(
        Component.mean.desc()).all()
    result = [{'id': c.id, 'name': c.name, 'private': c.private, 'mean': c.mean,
               "nr_use": len(Logic.query.filter(or_(Logic.component_1_id == c.id, Logic.component_2_id == c.id)).all())}
              for c in components]
    return jsonify({"result": result}), 200


@api.route('/rate', methods=['POST'])
@login_required
def rate():
    cid = request.json['cid']
    amount = int(request.json['amount'])
    star = Star.query.filter(and_(Star.component_id == cid, Star.user_id == current_user.id)).one_or_none()
    count = len(Star.query.filter_by(component_id=cid).all())
    component = Component.query.get(cid)
    if star:
        component.mean = (component.mean * count - star.amount + amount) / count
        star.amount = amount
    else:
        star = Star(component_id=cid, user_id=current_user.id, amount=amount)
        component.mean = (component.mean * count + amount) / (count + 1)
        db.session.add(star)
    db.session.commit()
