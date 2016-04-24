#  python imports
from sqlalchemy.exc import IntegrityError
# flask imports
from flask import Blueprint, request, jsonify, abort
# project imports
from application.models.logic import Logic
from application.extensions import db

__all__ = ['api']
api = Blueprint('project.api1', __name__, url_prefix='/api/v1/project')


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
