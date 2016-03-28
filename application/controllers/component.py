# python imports
import os
import re
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
# project imports
from application.models.component import Component
from application.forms.component import CreateComponentForm, UploadForm, EditForm
from application.extensions import db

__all__ = ['component']
component = Blueprint('component', __name__,url_prefix='/component')


@component.route('/list', methods=['GET'])
@login_required
def list_components():
    form = CreateComponentForm(request.form)
    c = Component.query.filter_by(owner=current_user.id).all()
    return render_template('component/list.html', components=c, form=form)


@component.route('/create', methods=['POST'])
@login_required
def create():
    form = CreateComponentForm(request.form)
    if form.validate():
        new_component = Component(name=form.name.data, owner=current_user.id)
        db.session.add(new_component)
        db.session.commit()
        return redirect(url_for('component.list_components'))
    flash('creation failed')
    return redirect(url_for('component.list_components'))


@component.route('/view/<int:cid>', methods=['GET'])
@login_required
def view(cid):
    c = Component.query.filter_by(id=cid).one_or_none()
    if current_user.id != c.owner:
        return abort(403)
    upload_form = UploadForm()
    edit_form = EditForm()
    regex = re.compile(r'\d+_(v(.+)\..+)')
    edit_form.deploy_version.choices = [(regex.match(f).group(2), regex.match(f).group(1)) for f in c.component_files()]
    return render_template('component/view.html', upload_form=upload_form, edit_form=edit_form, component=c)


@component.route('/upload/<int:cid>', methods=['POST'])
@login_required
def upload(cid):
    form = UploadForm()
    c = Component.query.filter_by(id=cid).one_or_none()
    if current_user.id != c.owner:
        return abort(403)
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        file_type = filename.rsplit('.', 1)[1]
        if file_type in current_app.config['ALLOWED_EXTENSIONS']:
            form.file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                             'components', '%s_v%s.%s' % (str(cid), form.version.data, file_type)))
            c.deploy_version = form.version.data
            db.session.commit()
            return redirect(url_for('component.view', cid=cid))
        else:
            flash('wrong file type')
            return redirect(url_for('component.view', cid=cid))
    flash('invalid form')
    return redirect(url_for('component.view', cid=cid))


@component.route('/edit/<int:cid>', methods=['POST'])
@login_required
def edit(cid):
    c = Component.query.filter_by(id=cid).one_or_none()
    form = EditForm(request.form)
    regex = re.compile(r'\d+_(v(.+)\..+)')
    form.deploy_version.choices = [(regex.match(f).group(2), regex.match(f).group(1)) for f in c.component_files()]
    if current_user.id != c.owner:
        return abort(403)
    if form.validate():
        if form.deploy_version.data:
            c.deploy_version = form.deploy_version.data
            db.session.commit()
        if form.name.data:
            c.name = form.name.data
            db.session.commit()
        return redirect(url_for('component.view', cid=cid))
    flash('invalid form')
    return redirect(url_for('component.view', cid=cid))


@component.route('/delete/<int:cid>', methods=['POST'])
@login_required
def delete(cid):
    c = Component.query.filter_by(id=cid).one_or_none()
    if current_user.id != c.owner:
        return abort(403)
    for f in c.component_files():
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],'components', f))
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('component.list_components'))
