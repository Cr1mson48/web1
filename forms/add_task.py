from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class Addtask(FlaskForm):
    account = StringField('account', validators=[DataRequired()])
    ticker = StringField('ticker', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    price_buy = IntegerField('price_buy')
    remember_me = BooleanField('Продажа по условиям')
    price_sell = IntegerField('price_sell')
    sell = BooleanField('Продать 1 ордером')
    sell1 = BooleanField('Пока не продаст всё')
    time = StringField('time', validators=[DataRequired()])
    submit = SubmitField('Добавить')