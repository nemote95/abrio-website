from flask import Blueprint, render_template
from application.extensions import db

__all__ = ["main"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')
