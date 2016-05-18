# flask imports
from flask import Blueprint, request, jsonify, abort
# project imports
from application.models.logic import Logic
from application.models.project import Project
from application.models.component import Component
from application.extensions import db, redis

__all__ = ['api']
api = Blueprint('project.api1', __name__, url_prefix='/api/v1/project')


@api.route('/status', methods=['GET'])
def status():
    private_key = request.json['private_key']
    project = Project.query.filter_by(private_key=private_key).one_or_none()
    if project:
        return jsonify({"name": project.name, "is_running": redis.exists('abr:%s' % private_key),
                        "create_date": str(project.create_date)}), 200
    return jsonify(), 404


@api.route('/start', methods=['POST'])
def start():
    private_key = request.json['private_key']
    project = Project.query.filter_by(private_key=private_key).one_or_none()
    if project:
        if not redis.exists('abr:%s' % private_key):
            redis.set('abr:%s' % private_key, project.id)
            return jsonify(), 200
        else:
            return jsonify(), 409
    return jsonify(), 404


@api.route('/stop', methods=['POST'])
def stop():
    private_key = request.json['private_key']
    project = Project.query.filter_by(private_key=private_key).one_or_none()
    if project:
        if redis.exists('abr:%s' % private_key):
            redis.delete('abr:%s' % private_key)
            return jsonify(), 200
        else:
            return jsonify(), 409

    return jsonify(), 404


@api.route('/list_components', methods=['GET'])
def list_components():
    private_key = request.json['private_key']
    project = Project.query.filter_by(private_key=private_key).one_or_none()
    if project:
        logic = Logic.query.filter_by(project_id=project.id).all()
        components = []
        for l in logic:
            for cid in [l.component_1_id, l.component_2_id]:
                if cid:
                    c = Component.query.filter_by(id=cid).one().to_json()
                    if c not in components:
                        components.append(c)
        return jsonify({"result": components}), 200
    return jsonify(), 404


@api.route('/logic', methods=['POST'])
def define_logic():
    project_id = request.json['project_id']
    db.session.query(Logic).filter_by(project_id=project_id).delete()
    db.session.commit()

    relations = [dict(t) for t in set([tuple(d.items()) for d in request.json['relations']])]
    for relation in relations:
        # input-component
        if not relation['component_1_id'] and relation['component_2_id']:
            new_logic = Logic(project_id=project_id,
                              component_2_id=relation['component_2_id'],
                              message_type=relation['message_type'])
            db.session.add(new_logic)
        # output-component
        elif not relation['component_2_id'] and relation['component_1_id']:
            new_logic = Logic(project_id=project_id,
                              component_1_id=relation['component_1_id'],
                              message_type=relation['message_type'])
            db.session.add(new_logic)
        # component-component
        elif relation['component_2_id'] and relation['component_1_id']:
            new_logic = Logic(project_id=project_id,
                              component_1_id=relation['component_1_id'],
                              component_2_id=relation['component_2_id'],
                              message_type=relation['message_type'])
            db.session.add(new_logic)

        db.session.commit()
    return jsonify(), 201
