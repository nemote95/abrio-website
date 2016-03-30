# python imports
from sqlalchemy.orm.exc import NoResultFound
import re
# flask imports
from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_user, login_required, logout_user, current_user

# project imports
from application.extensions import db, email
from application.forms.user import RegistrationForm, LoginForm, EditProfileForm
from application.models.user import User

__all__ = ["user"]

user = Blueprint("user", __name__)


@user.before_app_request
def before_request():
    allowed_pattern = re.compile(r'(user\.|static|main\.).*')
    match=re.match(allowed_pattern, str(request.endpoint))
    if current_user.is_authenticated and \
            not current_user.confirmed \
            and not match:
        return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


@user.route('/resend_confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    email.send(current_user.email, 'Confirm Your Account',
               render_template('user/email/confirm.html', user=current_user, token=token))
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User()
        new_user.email = form.email.data
        new_user.password = form.password.data
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()
        email.send(new_user.email, 'Confirm Your Account',
                   render_template('user/email/confirm.html', user=new_user, token=token))
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


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
    try:
        user_page = User.query.filter_by(id=uid).one()
        return render_template('user/profile.html', user_page=user_page)
    except NoResultFound:
        abort(404)


@user.route('/edit_profile')
def edit_view():
    form = EditProfileForm(request.form)
    return render_template('user/edit.html', form=form)


@user.route('/edit', methods=['Post'])
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if form.validate():
        u = User.query.filter_by(id=current_user.id).one()
        print u
        if form.company.data:
            u.company = form.company.data
            db.session.commit()
        if form.name.data:
            u.name = form.name.data
            db.session.commit()
        if form.phone_number.data:
            u.phone_number = form.phone_number.data
            db.session.commit()
        if form.ssn.data:
            u.ssn = form.ssn.data
            db.session.commit()
        return redirect(url_for('user.info', uid=current_user.id))
    flash('invalid information')
    return redirect(url_for('user.edit_view', uid=current_user.id))
