from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Length
from wtforms import StringField,PasswordField,TextAreaField,SelectField
from project.models.users_model import Users

def get_experts():
    experts = Users.get_experts()
    expertlist = []
    for expert in experts:
        t = (str(expert['id']), expert['name'])
        expertlist.append(t)
    return expertlist

class AskForm(FlaskForm):
    question = TextAreaField("Question", validators=[InputRequired()])
    expert = SelectField("Experts", choices=get_experts())

class AnswerForm(FlaskForm):
    answer = TextAreaField("Answer",validators=[InputRequired()])