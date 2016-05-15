# coding=utf-8
# python imports
import os
import re
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
# project imports
from application.models.component import Component
from application.models.project import Project
from application.forms.component import CreateComponentForm, UploadForm
from application.extensions import db
from application.decorators import permission

__all__ = ['component']
component = Blueprint('component', __name__, url_prefix='/component')


@component.route('/<pid>/new', methods=['GET', 'POST'])
@permission(Project, 'pid')
@login_required
def create(pid, obj=None):
    form = CreateComponentForm(meta={'locales': ['fa']})
    if request.method == 'POST' and form.validate_on_submit():
        new_component = Component(name=form.name.data, owner_id=current_user.id, private=form.private.data,
                                  deploy_version=form.version.data)
        filename = secure_filename(form.file.data.filename)
        file_type = filename.rsplit('.', 1)[1]
        if file_type in current_app.config['ALLOWED_EXTENSIONS']:
            form.file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                             'components',
                                             '%s_v%s.%s' % (str(new_component.id), form.version.data, file_type)))
            db.session.add(new_component)
            db.session.commit()
            return redirect(url_for('component.view', pid=pid, cid=new_component.id))
        else:
            flash(u'.فرمت این فایل قابل پشتیبانی نیست')
            return redirect(url_for('component.create', pid=pid))
    return render_template('component/newcomponent.html', form=form, pid=pid)


@component.route('/<int:pid>/<int:cid>', methods=['GET'])
@component.route('/<int:cid>', methods=['GET'], defaults={'pid': 0})
@login_required
@permission(Component, 'cid')
def view(pid, cid, obj=None):
    upload_form = UploadForm(meta={'locales': ['fa']})
    regex = re.compile(r'\d+_(v(.+)\..+)')
    version_choices = [regex.match(f).group(2) for f in
                       obj.component_files()]
    if pid:
        return_to_project = pid
    else:
        return_to_project = None
    return render_template('component/view.html', upload_form=upload_form, version_choices=version_choices,
                           component=obj, return_to_project=return_to_project)


@component.route('/<int:cid>/upload', methods=['POST'])
@login_required
@permission(Component, 'cid')
def upload(cid, obj=None):
    form = UploadForm(meta={'locales': ['fa']})
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_type = filename.rsplit('.', 1)[1]
        if file_type in current_app.config['ALLOWED_EXTENSIONS']:
            form.file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                             'components', '%s_v%s.%s' % (str(cid), form.version.data, file_type)))
            obj.deploy_version = form.version.data
            db.session.commit()
            return redirect(url_for('component.view', cid=cid))
        else:
            flash(u'.فرمت این فایل قابل پشتیبانی نیست')
            return redirect(url_for('component.view', cid=cid))
    flash(u'.پرکردن فیلد ها اجباری است')
    return redirect(url_for('component.view', cid=cid))


