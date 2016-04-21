# python imports
from uuid import uuid4
from sqlalchemy import or_
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask.ext.login import current_user, login_required
# project imports
from application.models.project import Project
from application.models.component import Component
from application.models.logic import Logic
from application.forms.project import CreateProjectForm
from application.extensions import db, redis
from application.decorators import permission

__all__ = ['project']
project = Blueprint('project', __name__, url_prefix='/project')


@project.route('/', methods=['GET'])
@login_required
def list_projects():
    form = CreateProjectForm(request.form, meta={'locales': ['fa']})
    c = Project.query.filter_by(owner_id=current_user.id).all()
    return render_template('project/list.html', projects=c, form=form)


@project.route('/', methods=['POST'])
@login_required
def create():
    form = CreateProjectForm(request.form, meta={'locales': ['fa']})
    if form.validate():
        new_project = Project(name=form.name.data, owner_id=current_user.id, private_key=str(uuid4()))
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project.view', pid=new_project.id))
    return redirect(url_for('project.list_projects'))


@project.route('/<int:pid>/view', methods=['GET'])
@login_required
@permission(Project, 'pid')
def view(pid, obj=None):
    components_choices = [(c.id, c.name) for c in Component.query.filter(
        or_(Component.owner_id == current_user.id, Component.private == False)).all()]
    project_logic = Logic.query.filter_by(project_id=pid).all()
    logic_view = [(Component.query.filter_by(id=l.component_1_id).one_or_none(),
                   Component.query.filter_by(id=l.component_2_id).one_or_none(),
                   l.message_type, l.id) for l in project_logic]
    running = redis.exists('abr:%s' % obj.private_key)
    return render_template('project/view.html', project=obj, logic_view=logic_view,
                           components_choices=components_choices, running=running)


@project.route('/<int:pid>/run', methods=['POST'])
@login_required
@permission(Project, 'pid')
def run_project(pid, obj=None):
    if redis.exists('abr:%s' % obj.private_key):
        redis.delete('abr:%s' % obj.private_key)
    else:
        redis.set('abr:%s' % obj.private_key, pid)
    return redirect(url_for('project.view', pid=pid))


@project.route('/<int:lid>/delete', methods=['POST'])
@login_required
def delete_logic(lid):
    logic = Logic.query.filter_by(id=lid).one_or_none()
    if not logic:
        return abort(404)
    p = Project.query.filter_by(id=logic.project_id).one()
    if p.owner_id == current_user.id:
        db.session.delete(logic)
        db.session.commit()
        return redirect(url_for('project.view', pid=p.id))
    else:
        return abort(403)
