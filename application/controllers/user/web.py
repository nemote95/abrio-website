# python imports
from requests import ConnectionError
from sqlalchemy.orm.exc import NoResultFound
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature
# flask imports
from flask import Blueprint, render_template, redirect, request, url_for, flash, abort, current_app
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
    match = re.match(allowed_pattern, str(request.endpoint))
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
    try:
        email.send(current_user.email, 'Confirm Your Account',
                   render_template('user/email/confirm.html', user=current_user, token=token))
    except:
        flash('sending confirmation email failed,try again')
        return redirect('user.unconfirmed')
    flash('A confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = User(email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        token = new_user.generate_confirmation_token()
        try:
            email.send(new_user.email, 'Confirm Your Account',
                       render_template('user/email/confirm.html', user=new_user, token=token))
            db.session.commit()
        except ConnectionError:
            flash('sending confirmation email failed,try again')
            db.session.rollback()
            return render_template('user/register.html', form=form)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/confirm/<token>')
def confirm(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        try:
            current_user = User.query.filter_by(id=data.get('confirm')).one()
            if not current_user.confirmed:
                current_user.confirmed = True
                db.session.commit()
                flash('You have confirmed your account. Thanks!')
            else:
                flash('You have already confirmed your account.')
            login_user(current_user)
        except :
            flash('The confirmation link is invalid or has expired.')
    except BadSignature:
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
        if form.company.data:
            u.company = form.company.data
        if form.name.data:
            u.name = form.name.data
        if form.phone_number.data:
            u.phone_number = form.phone_number.data
        if form.ssn.data:
            u.ssn = form.ssn.data
        db.session.commit()
        return redirect(url_for('user.info', uid=current_user.id))
    flash('invalid information')
    return redirect(url_for('user.edit_view', uid=current_user.id))
