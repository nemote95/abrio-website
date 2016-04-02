from flask import Blueprint, render_template
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
