import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Listings(SqlAlchemyBase):
    __tablename__ = 'listings'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=True)
    text = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    time = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date,
                                     default=datetime.date.today)

    def __repr__(self):
        return "<Listings %r>" % self.id
