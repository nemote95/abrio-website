from wtforms import Form, StringField, SelectField, BooleanField, validators
from flask.ext.wtf import Form as WTFForm
from flask.ext.wtf.file import FileField, FileRequired


class CreateComponentForm(WTFForm):
    name = StringField('Component Name', [validators.DataRequired()])
    private = BooleanField('private', [validators.optional()])
    file = FileField('Component file', validators=[FileRequired()])
    version = StringField('version', [validators.DataRequired()])


class UploadForm(WTFForm):
    file = FileField('Component file', validators=[FileRequired()])
    version = StringField('version', [validators.DataRequired()])


class EditForm(Form):
    name = StringField('Component Name', validators=[validators.optional()])
    deploy_version = SelectField('deploy version', validators=[validators.optional()])


class SearchForm(Form):
    name = StringField('Component Name', [validators.DataRequired()])