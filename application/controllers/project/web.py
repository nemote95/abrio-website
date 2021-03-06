# coding=utf-8

from datetime import datetime
from uuid import uuid4
from sqlalchemy import or_
from json import dumps
import os
from werkzeug import secure_filename

from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app, send_from_directory
from flask.ext.login import current_user, login_required

from application.models.project import Project, TopProject
from application.models.component import Component
from application.models.logic import Logic
from application.forms.project import CreateProjectForm, UploadForm
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
        new_project = Project(name=form.name.data, owner_id=current_user.id, private_key=str(uuid4()),
                              create_date=datetime.utcnow())
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('project.view', pid=new_project.id))
    flash(u'.این فیلد اجباری است')
    return redirect(url_for('project.list_projects'))


@project.route('/<int:pid>', methods=['GET'])
@login_required
@permission(Project, 'pid')
def view(pid, obj=None):
    form = UploadForm(meta={'locales': ['fa']})

    project_logic = Logic.query.filter_by(project_id=pid).all()

    components_choices = []

    for l in project_logic:
        components = Component.query.filter(
            or_(Component.id == l.component_1_id, Component.id == l.component_2_id)).all()
        for c in components:
            if {"id": c.id, "name": c.name} not in components_choices:
                components_choices.append({"id": c.id, "name": c.name})

    components_list = Component.query.filter(
        or_(Component.owner_id == current_user.id, Component.private == False)).order_by(Component.mean.desc()).all()

    logic_view = [(Component.query.filter_by(id=l.component_1_id).one_or_none(),
                   Component.query.filter_by(id=l.component_2_id).one_or_none(),
                   l.message_type, l.id) for l in project_logic]

    running = redis.exists('abr:%s' % obj.private_key)
    return render_template('project/view.html', project=obj, logic_view=logic_view,
                           components_choices=dumps(components_choices), components_list=components_list,
                           running=running, form=form)


@project.route('/<int:pid>/run', methods=['POST'])
@login_required
@permission(Project, 'pid')
def run_project(pid, obj=None):
    if redis.exists('abr:%s' % obj.private_key):
        redis.delete('abr:%s' % obj.private_key)
    else:
        redis.set('abr:%s' % obj.private_key, pid)
    return redirect(url_for('project.view', pid=pid))


@project.route('/<int:pid>/upload_logo', methods=['POST'])
@login_required
def upload_logo(pid):
    form = UploadForm(meta={'locales': ['fa']})
    if form.validate_on_submit():
        filename = secure_filename(form.logo_image.data.filename)
        file_type = filename.rsplit('.', 1)[1]
        if file_type in ['png', 'jpg', 'jpeg']:
            form.logo_image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                                   'logos', '%s.png' % str(pid)))
            return redirect(url_for('project.view', pid=pid))
        else:
            flash(u'.فرمت این فایل قابل پشتیبانی نیست')
            return redirect(url_for('project.view', pid=pid))
    flash(u'.لوگویی آپلود نشده است')
    return redirect(url_for('project.view', pid=pid))


@project.route('/<int:pid>/logo')
@login_required
def logo(pid):
    return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'] + 'logos/', filename="%s.png" % str(pid))


@project.route('/<int:tpid>/image')
@login_required
def top_project_image(tpid):
    return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'] + 'top_projects/',
                               filename="%s.png" % str(tpid))


@project.route('/<int:tpid>/top')
@login_required
def top_project(tpid):
    project = TopProject.query.get(tpid)
    return render_template('project/view_top.html', project=project)
