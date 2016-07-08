# coding=utf-8
# python imports
from requests import ConnectionError
from sqlalchemy.orm.exc import NoResultFound
import re
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import BadSignature
from sqlalchemy import and_
# flask imports
from flask import Blueprint, render_template, redirect, request, url_for, flash, abort, current_app
from flask.ext.login import login_user, login_required, logout_user, current_user
# project imports
from application.extensions import db, email
from application.forms.user import RegistrationForm, LoginForm
from application.forms.project import CreateProjectForm
from application.models.user import User
from application.models.component import Component
from application.models.project import Project
from application.models.enums import Abilities

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
    url = url_for('user.confirm', token=token, _external=True)
    try:
        email.send(current_user.email, 'Confirm Your Account',
                   render_template('user/email/confirm.html', user=current_user, url=url))
    except ConnectionError:
        flash(u'.ارسال ایمیل تایید حساب کاربری با مشکل روبه رو شد.مجددا تلاش کنید')
        return redirect('user.unconfirmed')
    flash(u'.یک ایمیل تایید حساب کاربری برای شما ارسال شده است')
    return redirect(url_for('main.index'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form, meta={'locales': ['fa']})
    if request.method == 'POST' and form.validate():
        plain_email = re.match(re.compile("(.*)(@.*)"), form.email.data)
        user_email = plain_email.group(1).replace('.', '') + plain_email.group(2)

        new_user = User(email=user_email, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        new_user.add_ability(Abilities.TYPICAL)

        token = new_user.generate_confirmation_token()
        url = url_for('user.confirm', token=token, _external=True)
        try:
            email.send(new_user.email, 'Confirm Your Account',
                       render_template('user/email/confirm.html', user=new_user, url=url))
        except ConnectionError:
            flash(u'.ارسال ایمیل تایید حساب کاربری با مشکل روبه رو شد.مجددا تلاش کنید')
            db.session.rollback()
            return render_template('user/register.html', form=form)
        flash(u'.یک ایمیل تایید حساب کاربری برای شما ارسال شده است')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


@user.route('/confirm/<token>')
def confirm(token):
    serializer = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(
            token,
            max_age=current_app.config['EXPIRATION'])

        try:
            current_user = User.query.filter_by(id=user_id).one()
            if not current_user.confirmed:
                current_user.confirmed = True
                db.session.commit()
                flash(u'.حساب شما تایید شد')
            else:
                flash(u'.حساب شما قبلا تایید شده بود')
            login_user(current_user)
        except NoResultFound:
            flash(u'.لینک تاید حساب کاربری نامعتبر و یا منقضی می باشد')
    except BadSignature:
        flash(u'.لینک تاید حساب کاربری نامعتبر و یا منقضی می باشد')
    return redirect(url_for('main.index'))


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form, meta={'locales': ['fa']})
    if request.method == 'POST' and form.validate():
        plain_email = re.match(re.compile("(.*)(@.*)"), form.email.data)
        email = plain_email.group(1).replace('.', '') + plain_email.group(2)

        new_user = User.query.filter_by(email=email).first()
        if new_user is not None and new_user.verify_password(form.password.data):
            login_user(new_user)
            return redirect(request.args.get('next') or url_for('user.info'))
        flash(u'.آدرس ایمیل یا کلمه ی عبور نا معتبر است')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'.شما خارج شدید')
    return redirect(url_for('main.index'))


@user.route('/profile')
@login_required
def info():
    uid = request.args.get("uid")
    if not uid or long(uid) == current_user.id:
        user_page = User.query.filter_by(id=current_user.id).one()
        c = Component.query.filter(Component.owner_id == current_user.id).all()
        p = Project.query.filter_by(owner_id=current_user.id).all()
        form = CreateProjectForm(request.form, meta={'locales': ['fa']})
        return render_template('user/myprofile.html', user_page=user_page, components=c, projects=p, form=form)
    else:
        try:
            user_page = User.query.filter_by(id=uid).one()
            c = Component.query.filter(and_(Component.owner_id == user.id, Component.private == False)).all()
            return render_template('user/profile.html', user_page=user_page, components=c)
        except NoResultFound:
            return abort(404)
