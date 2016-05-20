from wtforms import Form, StringField, SelectField, validators
from flask.ext.wtf import Form as WTFForm
from flask.ext.wtf.file import FileField, FileRequired

class CreateProjectForm(Form):
    name = StringField('Project Name', [validators.DataRequired()])


class UploadForm(WTFForm):
    logo_image = FileField('logo_image', validators=[FileRequired()])