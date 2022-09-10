from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class APIForm(FlaskForm):
    name_account = StringField('name', validators=[DataRequired()])
    apiKey = StringField('apiKey', validators=[DataRequired()])
    secretKey = StringField('secretKey', validators=[DataRequired()])
    PassPhrase = StringField('secretKey', validators=[DataRequired()])
    submit = SubmitField('Добавить')