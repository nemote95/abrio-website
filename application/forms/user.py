from wtforms import Form, StringField, PasswordField, validators

from wtforms import ValidationError
from application.models.user import User


class RegistrationForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired(), validators.Length(min=6)])
    confirm = PasswordField(u'Confirm password', validators=[validators.EqualTo('password')])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired(), validators.Length(min=6)])


class EditProfileForm(Form):
    name = StringField('Name', [validators.optional()])
    company = StringField('Company', [validators.optional()])
    phone_number = StringField('Phone Number', [validators.optional(), validators.Regexp('\d{6,13}')])
    ssn = StringField('SSN', [validators.optional(), validators.Regexp('\d{10}')])
