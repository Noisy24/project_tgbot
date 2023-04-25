import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    users_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    company_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    model_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer)
