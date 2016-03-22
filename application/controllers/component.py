# flask imports
from flask import Blueprint, request, render_template
# project imports
from application.models.component import Component
from flask.ext.login import current_user, login_required

__all__ = ['component']
component = Blueprint('component', __name__)


@component.route('/view', methods=['GET'])
@login_required
def view():
    c = Component.query.filter_by(owner=current_user.id).all()
    return render_template('component/view.html', components=c)
