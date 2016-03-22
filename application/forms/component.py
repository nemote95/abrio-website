from wtforms import Form, StringField,  validators


class CreateComponentForm(Form):
    name = StringField('Component Name', [validators.DataRequired()])
