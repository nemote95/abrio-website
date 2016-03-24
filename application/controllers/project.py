# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app
from flask.ext.login import current_user, login_required
# project imports
from application.models.project import Project
from application.models.Logic import Logic
from application.forms.project import CreateProjectForm
from application.extensions import db

__all__ = ['project']
project = Blueprint('project', __name__, url_prefix='/project')


@project.route('/list', methods=['GET'])
@login_required
def list_projects():
    form = CreateProjectForm(request.form)
    c = Project.query.filter_by(owner=current_user.id).all()
    return render_template('project/list.html', projects=c, form=form)


@project.route('/create', methods=['POST'])
@login_required
def create():
    form = CreateProjectForm(request.form)
    if form.validate():
        new_project = Project(name=form.name.data, owner=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project.list_projects'))
    flash('creation failed')
    return redirect(url_for('project.list_projects'))
