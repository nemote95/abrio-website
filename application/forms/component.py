# flask imports
from wtforms import Form, StringField, SelectField, BooleanField, validators
from flask.ext.wtf import Form as WTFForm
from flask.ext.wtf.file import FileField, FileRequired


class CreateComponentForm(WTFForm):
    name = StringField('Component Name', [validators.DataRequired()])
    private = BooleanField('private', [validators.optional()])
    """set datarequired validator"""
    version = StringField('version')


class UploadForm(WTFForm):
    file = FileField('Component file', validators=[FileRequired()])
    """set datarequired validator"""
    version = StringField('version')


class SearchForm(Form):
    name = StringField('Component Name', [validators.DataRequired()])
