from wtforms import Form, StringField, validators


class CreateProjectForm(Form):
    name = StringField('Project Name', [validators.DataRequired()])

