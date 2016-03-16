# flask imports
from flask import Blueprint, render_template, redirect, request, url_for, flash
# project imports
from application.extensions import db
from application.forms.user import RegistrationForm
from application.models.user import User


__all__ = ["user"]

user = Blueprint("user", __name__)


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)

