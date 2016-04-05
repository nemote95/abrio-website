# flask imports
from flask import Blueprint, request, jsonify
# project imports
from application.models.logic import Logic
from application.extensions import db

__all__ = ['api']
api = Blueprint('project.api1', __name__, url_prefix='/api/v1/project')


@api.route('/define_logic', methods=['POST'])
def define_logic():
    project_id = request.json['project_id']
    relations = request.json['relations']
    for relation in relations:
        new_logic = Logic(project_id=project_id,
                          component_1_id=relation['component_1_id'],
                          component_2_id=relation['component_2_id'],
                          message_type=relation['message_type'])
        db.session.add(new_logic)
        db.session.commit()

    return jsonify(), 201
