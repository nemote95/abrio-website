# coding=utf-8
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


@component.route('/', methods=['GET'])
@login_required
def list_components():
    create_form = CreateComponentForm(request.form, meta={'locales': ['fa']})
    search_form = SearchForm(request.form, meta={'locales': ['fa']})
    c = Component.query.filter(or_(Component.owner_id == current_user.id, Component.private == False)).all()
    return render_template('component/list.html', components=c, create_form=create_form, search_form=search_form)


@component.route('/', methods=['POST'])
@login_required
def create():
    form = CreateComponentForm(request.form, meta={'locales': ['fa']})
    if form.validate():
        new_component = Component(name=form.name.data, owner_id=current_user.id, private=form.private.data)
        db.session.add(new_component)
        db.session.commit()
        return redirect(url_for('component.view', cid=new_component.id))
    return redirect(url_for('component.list_components'))


@component.route('/<int:cid>/view', methods=['GET'])
@login_required
@permission(Component, 'cid')
def view(cid, obj=None):
    upload_form = UploadForm(meta={'locales': ['fa']})
    regex = re.compile(r'\d+_(v(.+)\..+)')
    version_choices = [regex.match(f).group(2) for f in
                                        obj.component_files()]
    return render_template('component/view.html', upload_form=upload_form, version_choices=version_choices, component=obj)


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


@component.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    create_form = CreateComponentForm(request.form, meta={'locales': ['fa']})
    search_form = SearchForm(request.form, meta={'locales': ['fa']})
    if request.method == 'POST' and search_form.validate():
        c = Component.query.filter(and_(Component.name.contains(search_form.name.data),
                                        or_(Component.private == False, Component.owner_id == current_user.id))).all()
    else:
        c = Component.query.filter_by(owner_id=current_user.id).all()
    return render_template('component/list.html', components=c, create_form=create_form, search_form=search_form)
