import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Api_account(SqlAlchemyBase):
    __tablename__ = 'api_account'
    id = sqlalchemy.Column(sqlalchemy.Integer)
    market = sqlalchemy.Column(sqlalchemy.String, nullable=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    api = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    secret = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    passPhrase = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return "<Api_account %r>" % self.id