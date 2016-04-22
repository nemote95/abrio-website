# flask imports
from flask import Blueprint, request, jsonify,abort
# project imports
from application.models.logic import Logic
from application.extensions import db

__all__ = ['api']
api = Blueprint('project.api1', __name__, url_prefix='/api/v1/project')


@api.route('/logic', methods=['POST'])
def define_logic():
    project_id = request.json['project_id']
    relations = request.json['relations']
    for relation in relations:
        if relation['component_1_id']=="Input" and relation['component_2_id']=="Output":
            return jsonify(),404
        elif relation['component_1_id'] == "Input":
            new_logic = Logic(project_id=project_id,
                              component_2_id=relation['component_2_id'],
                              message_type=relation['message_type'])
        elif relation['component_2_id'] == "Output":
            new_logic = Logic(project_id=project_id,
                              component_1_id=relation['component_1_id'],
                              message_type=relation['message_type'])
        else:
            new_logic = Logic(project_id=project_id,
                              component_1_id=relation['component_1_id'],
                              component_2_id=relation['component_2_id'],
                              message_type=relation['message_type'])
        db.session.add(new_logic)
        db.session.commit()
    return jsonify(), 201
