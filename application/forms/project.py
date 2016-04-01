from wtforms import Form, StringField, SelectField, validators


class CreateProjectForm(Form):
    name = StringField('Project Name', [validators.DataRequired()])


class LogicForm(Form):
    component1 = SelectField('Component No1', coerce=int, validators=[validators.DataRequired()])
    component2 = SelectField('Component No2', coerce=int, validators=[validators.DataRequired()])
    message_type = SelectField('Message Types', choices=[('BasicEvent', 'BasicEvent'), ('type_b', 'type_b')],
                               validators=[validators.DataRequired()])
