# python imports
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask.ext.login import current_user, login_required
# project imports
from application.models.project import Project
from application.models.component import Component
from application.models.logic import Logic
from application.forms.project import CreateProjectForm, LogicForm
from application.extensions import db, redis

__all__ = ['project']
project = Blueprint('project', __name__, url_prefix='/project')


@project.route('/list', methods=['GET'])
@login_required
def list_projects():
    form = CreateProjectForm(request.form)
    c = Project.query.filter_by(owner_id=current_user.id).all()
    return render_template('project/list.html', projects=c, form=form)


@project.route('/create', methods=['POST'])
@login_required
def create():
    form = CreateProjectForm(request.form)
    if form.validate():
        new_project = Project(name=form.name.data, owner_id=current_user.id, private_key=str(uuid4()))
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project.list_projects'))
    flash('creation failed')
    return redirect(url_for('project.list_projects'))


@project.route('/view/<int:pid>', methods=['GET'])
@login_required
def view(pid):
    p = Project.query.filter_by(id=pid).one_or_none()
    if current_user.id != p.owner_id:
        return abort(403)
    logic_form = LogicForm(request.form)
    logic_form.component1.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    logic_form.component2.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    project_logic = Logic.query.filter_by(project_id=pid).all()
    logic_view = [(Component.query.filter_by(id=l.component_1_id).one_or_none(),
                   Component.query.filter_by(id=l.component_2_id).one_or_none(), l.message_type) for l in project_logic]
    running = redis.exists('abr:%s' % p.private_key)
    return render_template('project/view.html', project=p, logic_form=logic_form, logic_view=logic_view,
                           running=running)


@project.route('/define_logic/<int:pid>', methods=['POST'])
@login_required
def define_logic(pid):
    p = Project.query.filter_by(id=pid).one_or_none()
    if current_user.id != p.owner_id:
        return abort(403)
    logic_form = LogicForm(request.form)
    logic_form.component1.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    logic_form.component2.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    if logic_form.validate():
        try:
            new_logic = Logic(project_id=p.id, component_1_id=logic_form.component1.data,
                              component_2_id=logic_form.component2.data, message_type=logic_form.message_type.data)
            db.session.add(new_logic)
            db.session.commit()
        except IntegrityError:
            flash('you have already defined this logic')
        return redirect(url_for('project.view', pid=pid))
    flash('invalid logic')
    return redirect(url_for('project.view', pid=pid))


@project.route('/run/<int:pid>', methods=['POST'])
@login_required
def run_project(pid):
    p = Project.query.filter_by(id=pid).one_or_none()
    if current_user.id != p.owner_id:
        return abort(403)
    if redis.exists('abr:%s' % p.private_key):
        redis.delete('abr:%s' % p.private_key)
    else:
        redis.set('abr:%s' % p.private_key, pid)
    return redirect(url_for('project.view', pid=pid))
