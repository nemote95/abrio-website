from flask import Blueprint, render_template, send_from_directory, current_app
from flask.ext.login import login_required, current_user
from application.models.component import Component
from application.models.project import TopProject
from application.models.logic import Logic
from sqlalchemy import or_
import random

__all__ = ["main"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/downloads')
@login_required
def downloads():
    return render_template('downloads.html')


@main.route('/download-sdk')
@login_required
def download_sdk():
    return send_from_directory(directory=current_app.config['SDK_DIRECTORY'],
                               filename=current_app.config['SDK_FILENAME'], as_attachment=True)


@main.route('/explore', methods=['GET'])
@login_required
def explore():
    top_projects_all = TopProject.query.all()
    if len(top_projects_all) > 2:
        random_numbers = random.sample(xrange(0, len(top_projects_all)), 3)
        random_top_projects = [top_projects_all[i] for i in random_numbers]
    else:
        random_top_projects = top_projects_all
    components = Component.query.filter(
        or_(Component.owner_id == current_user.id, Component.private == False)).order_by(Component.mean.desc()).all()
    details = [{'id': c.id, 'name': c.name, 'private': c.private, 'mean': c.mean,
                "nr_use": len(
                    Logic.query.filter(or_(Logic.component_1_id == c.id, Logic.component_2_id == c.id)).all())}
               for c in components]

    return render_template('explore.html', details=details, random_top_projects=random_top_projects)
