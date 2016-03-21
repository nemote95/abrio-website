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


@api.route('/upload', methods=['POST'])
def upload_component():
    token = request.headers.get('private key')
    version = request.headers.get('version')
    file = request.files['files']
    file_type = file.filename.rsplit('.', 1)[1]
    component = Component.verify_token(token)

    try:
        component.deploy_version = version
        db.session.commit()
    except:
        return abort(401)

    if file_type in current_app.config['ALLOWED_EXTENSIONS']:
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                               'components', '%s_v%s.%s' % (str(component.id), version, file_type)))
        return 'successfully uploaded', 200
    else:
        return abort(422)
