# flask imports
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, login_required,logout_user, current_user

# project imports
from application.extensions import db
from application.forms.user import RegistrationForm, LoginForm
from application.models.user import User

__all__ = ["user"]

user = Blueprint("user", __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(email=form.email.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form), 201


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User.query.filter_by(email=form.email.data).first()
        if new_user is not None and new_user.verify_password(form.password.data):
            login_user(new_user)
            return redirect(request.args.get('next') or url_for('main.panel'))
        flash('Invalid username or password.')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@user.route('/profile/<int:uid>')
def info(uid):
    user_page = User.query.filter_by(id=current_user.id).one()
    return render_template('user/profile.html', user_page=current_user)