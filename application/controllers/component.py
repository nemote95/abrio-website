# python imports
import os
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
# project imports
from application.models.component import Component
from application.forms.component import CreateComponentForm, UploadForm, EditForm
from application.extensions import db

__all__ = ['component']
component = Blueprint('component', __name__)


@component.route('/list', methods=['GET'])
@login_required
def list():
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
        return redirect(url_for('component.list'))
    flash('creation failed')
    return redirect(url_for('component.list'))


@component.route('/view/<int:cid>', methods=['GET'])
@login_required
def view(cid):
    c = Component.query.filter_by(id=cid).one_or_none()
    if current_user.id != c.owner:
        return abort(403)
    upload_form = UploadForm()
    edit_form = EditForm()
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
            c.deploy_version=form.version.data
            db.session.commit()
        else:
            flash('wrong file type')
    flash('invalid form')
    return redirect(url_for('component.view', cid=cid))


@component.route('/edit/<int:cid>', methods=['POST'])
@login_required
def edit(cid):
    form = EditForm(request.form)
    c = Component.query.filter_by(id=cid).one_or_none()
    if current_user.id != c.owner:
        return abort(403)
    print form.validate()
    if form.validate():
        c.deploy_version=form.deploy_version.data
        c.name=form.name.data
        db.session.commit()
        flash('successfully updated')
    return redirect(url_for('component.view', cid=cid))