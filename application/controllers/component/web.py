# coding=utf-8
# python imports
import os
import re
from sqlalchemy import or_
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
# project imports
from application.models.component import Component
from application.models.logic import Logic
from application.forms.component import CreateComponentForm, UploadForm
from application.extensions import db
from application.decorators import permission

__all__ = ['component']
component = Blueprint('component', __name__, url_prefix='/component')


@component.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateComponentForm(meta={'locales': ['fa']})
    if request.method == 'POST' and form.validate_on_submit():
        back = request.args.get('back')
        new_component = Component(name=form.name.data, owner_id=current_user.id, private=form.private.data)
        filename = secure_filename(form.file.data.filename)
        file_type = filename.rsplit('.', 1)[1]
        if file_type in current_app.config['ALLOWED_EXTENSIONS']:
            db.session.add(new_component)
            db.session.commit()
            """apply deploy version again"""
            form.file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                             'components',
                                             '%s.%s' % (str(new_component.id), file_type)))
            return redirect(url_for('component.view', cid=new_component.id, back=back))
        else:
            flash(u'.فرمت این فایل قابل پشتیبانی نیست')
            return redirect(url_for('component.create'))
    return render_template('component/newcomponent.html', form=form)


@component.route('/<int:cid>', methods=['GET'])
@login_required
@permission(Component, 'cid')
def view(cid, obj=None):
    back = request.args.get('back') or request.referrer
    upload_form = UploadForm(meta={'locales': ['fa']})
    regex = re.compile(r'\d+_(v(.+)\..+)')
    """apply deploy version again"""
    # version_choices = [regex.match(f).group(2) for f in obj.component_files()]

    nr_use = len(Logic.query.filter(or_(Logic.component_1_id == cid, Logic.component_2_id == cid)).all())
    return render_template('component/view.html', upload_form=upload_form,
                           component=obj, nr_use=nr_use, back=back)


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
                                             'components', '%s.%s' % (str(cid), file_type)))
            """apply deploy version again"""
            # obj.deploy_version = form.version.data
            db.session.commit()
            return redirect(url_for('component.view', cid=cid))
        else:
            flash(u'.فرمت این فایل قابل پشتیبانی نیست')
            return redirect(url_for('component.view', cid=cid))
    flash(u'.پرکردن فیلد ها اجباری است')
    return redirect(url_for('component.view', cid=cid))


@component.route('/<int:cid>/delete', methods=['GET'])
@login_required
@permission(Component, 'cid')
def delete(cid, obj=None):
    if not Logic.query.filter(or_(Logic.component_1_id == cid, Logic.component_2_id == cid)).all():
        files = obj.component_files()
        for f in files:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                   'components', f))
        db.session.delete(obj)
        db.session.commit()
        return redirect(url_for('user.profile', uid=current_user.id))
    else:
        flash(u'.از این کامپوننت در یک یا چند پروژه استفاده شده است')
        return redirect(url_for('component.view', cid=cid))
