from flask import Blueprint, render_template, send_from_directory, current_app
from flask.ext.login import login_required

__all__ = ["main"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/mypanel')
@login_required
def panel():
    return render_template('panel.html')


@main.route('/download')
@login_required
def download():
    return send_from_directory(directory=current_app.config['SDK_DIRECTORY'],
                               filename=current_app.config['SDK_FILENAME'], as_attachment=True)
