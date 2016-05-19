from flask import Blueprint, render_template, send_from_directory, current_app,request
from flask.ext.login import login_required,current_user
from application.models.component import Component
from sqlalchemy import or_

__all__ = ["main"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/home')
@login_required
def home():
    return render_template('home.html')


@main.route('/download')
@login_required
def download():
    return send_from_directory(directory=current_app.config['SDK_DIRECTORY'],
                               filename=current_app.config['SDK_FILENAME'], as_attachment=True)


@main.route('/explore', methods=['GET'])
@login_required
def explore():
    c = Component.query.filter(or_(Component.owner_id == current_user.id, Component.private == False)).all()
    return render_template('explore.html', components=c)



