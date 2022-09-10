import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Tasks(SqlAlchemyBase):
    __tablename__ = 'Tasks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_users = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    ticker = sqlalchemy.Column(sqlalchemy.String(30), nullable=True)
    buy = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    sell = sqlalchemy.Column(sqlalchemy.Text)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price_buy = sqlalchemy.Column(sqlalchemy.Integer)
    price_sell = sqlalchemy.Column(sqlalchemy.Integer)
    data = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date,
                                     default=datetime.date.today)
