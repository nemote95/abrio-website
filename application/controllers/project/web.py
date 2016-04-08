# python imports
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
from application.decorators import permission

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
        try:
            db.session.commit()
            return redirect(url_for('project.view', pid=new_project.id))
        except:
            db.session.rollback()
    flash('creation failed')
    return redirect(url_for('project.list_projects'))


@project.route('/view/<int:pid>', methods=['GET'])
@login_required
@permission(Project, 'pid')
def view(pid, obj=None):
    logic_form = LogicForm(request.form)
    logic_form.component1.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    logic_form.component2.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    project_logic = Logic.query.filter_by(project_id=pid).all()
    logic_view = [(Component.query.filter_by(id=l.component_1_id).one_or_none(),
                   Component.query.filter_by(id=l.component_2_id).one_or_none(), l.message_type) for l in project_logic]
    running = redis.exists('abr:%s' % obj.private_key)
    return render_template('project/view.html', project=obj, logic_form=logic_form, logic_view=logic_view,
                           running=running)


@project.route('/define_logic/<int:pid>', methods=['POST'])
@login_required
@permission(Project, 'pid')
def define_logic(pid, obj=None):
    logic_form = LogicForm(request.form)
    logic_form.component1.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    logic_form.component2.choices = [(c.id, c.name) for c in Component.query.filter_by(owner_id=current_user.id).all()]
    if logic_form.validate():
        new_logic = Logic(project_id=obj.id, component_1_id=logic_form.component1.data,
                              component_2_id=logic_form.component2.data, message_type=logic_form.message_type.data)
        db.session.add(new_logic)
        try:
            db.session.commit()
            return redirect(url_for('project.view', pid=pid))
        except:
            db.session.rollback()
            flash('creation failed')
            return redirect(url_for('project.view', pid=pid))
    flash('invalid logic')
    return redirect(url_for('project.view', pid=pid))


@project.route('/run/<int:pid>', methods=['POST'])
@login_required
@permission(Project, 'pid')
def run_project(pid, obj=None):
    if redis.exists('abr:%s' % obj.private_key):
        redis.delete('abr:%s' % obj.private_key)
    else:
        redis.set('abr:%s' % obj.private_key, pid)
    return redirect(url_for('project.view', pid=pid))
