# python imports
from sqlalchemy.exc import IntegrityError
# flask imports
from flask_admin import AdminIndexView as oldAdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.rediscli import RedisCli
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_admin.helpers import get_redirect_target
from flask import redirect, current_app, flash, abort, request
from flask_login import current_user
# project imports
import os
from werkzeug import secure_filename
from application.forms.project import CreateTopProjectForm, EditTopProjectForm


class AdminIndexView(oldAdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminModelView(ModelView):
    details_modal = True
    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminRedis(RedisCli):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminFile(FileAdmin):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AdminTopProjectView(AdminModelView):
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        form = CreateTopProjectForm()
        return_url = get_redirect_target() or self.get_url('.index_view')
        if request.method == 'POST' and form.validate_on_submit():
            filename = secure_filename(form.image.data.filename)
            file_type = filename.rsplit('.', 1)[1]
            if file_type in ['png', 'jpg', 'jpeg']:
                new_top_project = self.model(name=form.name.data, description=form.description.data)
                self.session.add(new_top_project)
                self.session.commit()
                form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                                  'top_projects', '%s.png' % str(new_top_project.id)))
                return redirect(return_url)
            else:
                flash('this file is not supported')
        return self.render('admin/create_top_project.html', form=form)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        top_project = self.get_one(id)

        form = EditTopProjectForm(description=top_project.description, name=top_project.name)

        if request.method == 'POST' and form.validate_on_submit():
            top_project.name = form.name.data
            top_project.description = form.description.data
            self.session.commit()
            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                file_type = filename.rsplit('.', 1)[1]
                if file_type in ['png', 'jpg', 'jpeg']:

                    form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                                      'top_projects', '%s.png' % str(top_project.id)))
                else:
                    flash('this file is not supported')
                    return self.render('admin/edit_top_project.html', form=form)

            return redirect(return_url)

        return self.render('admin/edit_top_project.html', form=form)

    @expose('/delete/', methods=['POST'])
    def delete_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.form['id']
        if id is None:
            return redirect(return_url)
        top_project = self.get_one(id)
        self.session.delete(top_project)
        self.session.commit()

        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'top_projects', '%s.png' % str(id))
        if os.path.exists(image_path):
            os.remove(image_path)

        return redirect(return_url)


class AdminComponentView(AdminModelView):
    @expose('/delete/', methods=['POST'])
    def delete_view(self):
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.form['id']
        if id is None:
            return redirect(return_url)
        component = self.get_one(id)
        upload_files = component.component_files()
        try:
            self.session.delete(component)
            self.session.commit()
            for f in upload_files:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],
                                       'components', f))
        except IntegrityError:
            flash('Integrity error. this component is used in some project', 'error')

        return redirect(return_url)


class AdminProjectView(AdminModelView):
    @expose('/delete/', methods=['POST'])
    def delete_view(self):
        from application.models.logic import Logic
        return_url = get_redirect_target() or self.get_url('.index_view')

        id = request.form['id']
        if id is None:
            return redirect(return_url)
        project = self.get_one(id)
        self.session.query(Logic).filter_by(project_id=id).delete()
        self.session.delete(project)
        self.session.commit()

        logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'logos', '%s.png' % str(id))
        if os.path.exists(logo_path):
            os.remove(logo_path)

        return redirect(return_url)
