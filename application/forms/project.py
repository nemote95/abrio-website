from wtforms import Form, StringField, SelectField, validators


class CreateProjectForm(Form):
    name = StringField('Project Name', [validators.DataRequired()])

