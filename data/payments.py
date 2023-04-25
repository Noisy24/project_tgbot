import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Payment(SqlAlchemyBase):
    __tablename__ = 'payments'

    bill_id = sqlalchemy.Column(sqlalchemy.Integer)
    payer_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Integer)

