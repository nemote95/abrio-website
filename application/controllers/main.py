# -*- coding: utf-8 -*-
"""
@author: Negmo
"""
from flask import Blueprint, render_template

__all__ = ["main"]

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')
