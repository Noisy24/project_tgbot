import sqlalchemy
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    users_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    balance = sqlalchemy.Column(sqlalchemy.Integer)
    basket = sqlalchemy.Column(sqlalchemy.String)
