from wtforms import Form, StringField, validators, SubmitField
from flask.ext.wtf import Form as WTFForm
from flask.ext.wtf.file import FileField, FileRequired


class CreateComponentForm(Form):
    name = StringField('Component Name', [validators.DataRequired()])


class UploadForm(WTFForm):
    file = FileField('Component file', validators=[FileRequired()])
    version = StringField('version', [validators.DataRequired()])
