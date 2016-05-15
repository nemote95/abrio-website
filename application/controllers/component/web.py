# python imports
import os
import re
from sqlalchemy import or_, and_
# flask imports
from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, current_app
from flask.ext.login import current_user, login_required
from werkzeug import secure_filename
# project imports
from application.models.component import Component
from application.forms.component import CreateComponentForm, UploadForm, EditForm, SearchForm
from application.extensions import db
from application.decorators import permission

__all__ = ['component']
component = Blueprint('component', __name__, url_prefix='/component')


@component.route('/list', methods=['GET'])
@login_required
def list_components():
    create_form = CreateComponentForm(request.form)
    search_form = SearchForm(request.form)
    c = Component.query.filter(or_(Component.owner_id == current_user.id, Component.private == False)).all()
    return render_template('component/list.html', components=c, create_form=create_form, search_form=search_form)
@component.route('/create', methods=['POST'])
@login_required
def create():
    form = CreateComponentForm(request.form)
    if form.validate():
        new_component = Component(name=form.name.data, owner_id=current_user.id, private=form.private.data)
        try:
            db.session.add(new_component)
            db.session.commit()
            return redirect(url_for('component.view', cid=new_component.id))
        except:
            db.session.rollback()
            flash('creation failed')
    return redirect(url_for('component.list_components'))


@component.route('/view/<int:cid>', methods=['GET'])
@login_required
@permission(Component, 'cid')
def view(cid, obj=None):
    upload_form = UploadForm()
    edit_form = EditForm()
    regex = re.compile(r'\d+_(v(.+)\..+)')
    edit_form.deploy_version.choices = [(regex.match(f).group(2), regex.match(f).group(1)) for f in
                                        obj.component_files()]
    return render_template('component/view.html', upload_form=upload_form, edit_form=edit_form, component=obj)


@component.route('/upload/<int:cid>', methods=['POST'])
@login_required
@permission(Component, 'cid')
def upload(cid, obj=None):
    form = UploadForm()
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
            flash('wrong file type')
            return redirect(url_for('component.view', cid=cid))
    flash('invalid form')
    return redirect(url_for('component.view', cid=cid))


@component.route('/edit/<int:cid>', methods=['POST'])
@login_required
@permission(Component, 'cid')
def edit(cid, obj=None):
    form = EditForm(request.form)
    regex = re.compile(r'\d+_(v(.+)\..+)')
    form.deploy_version.choices = [(regex.match(f).group(2), regex.match(f).group(1)) for f in obj.component_files()]
    if form.validate():
        if form.deploy_version.data:
            obj.deploy_version = form.deploy_version.data
        if form.name.data:
            obj.name = form.name.data
        db.session.commit()
        return redirect(url_for('component.view', cid=cid))
    flash('invalid form')
    return redirect(url_for('component.view', cid=cid))


@component.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    create_form = CreateComponentForm(request.form)
    search_form = SearchForm(request.form)
    if request.method == 'POST' and search_form.validate():
        c = Component.query.filter(and_(Component.name.contains(search_form.name.data),
                                        or_(Component.private == False, Component.owner_id == current_user.id))).all()
    else:
        c = Component.query.filter_by(owner_id=current_user.id).all()
    return render_template('component/list.html', components=c, create_form=create_form, search_form=search_form)
