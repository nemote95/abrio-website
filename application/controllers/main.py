# -*- coding: utf-8 -*-

from flask import Blueprint, render_template

__all__ = ["main"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')
