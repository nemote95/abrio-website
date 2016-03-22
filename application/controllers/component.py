# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask.ext.login import current_user, login_required
# project imports
from application.models.component import Component
from application.forms.component import CreateComponentForm
from application.extensions import db

__all__ = ['component']
component = Blueprint('component', __name__)


@component.route('/view', methods=['GET'])
@login_required
def view():
    form = CreateComponentForm(request.form)
    c = Component.query.filter_by(owner=current_user.id).all()
    return render_template('component/view.html', components=c, form=form)


@component.route('/create', methods=['POST'])
@login_required
def create():
    form = CreateComponentForm(request.form)
    if form.validate():
        new_component = Component(name=form.name.data, owner=current_user.id)
        db.session.add(new_component)
        db.session.commit()
        return redirect(url_for('component.view'))
    flash('creation failed')
    return redirect(url_for('component.view'))