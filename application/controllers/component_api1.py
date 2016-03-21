# python imports
import os
# flask imports
from flask import abort, Blueprint, jsonify, request, current_app
# project imports
from application.models.component import Component
from application.extensions import db


__all__ = ['api']
api = Blueprint('component.api1', __name__, url_prefix='/api/v1/component')


@api.route('/create', methods=['POST'])
def create_component():
    name = request.json['name']
    new_component = Component(name=name)
    db.session.add(new_component)
    db.session.commit()
    return jsonify(token=new_component.generate_token()), 201