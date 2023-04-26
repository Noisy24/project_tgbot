import sqlalchemy
from data.db_session import SqlAlchemyBase


class Payment(SqlAlchemyBase):
    __tablename__ = 'payments'

    bill_id = sqlalchemy.Column(sqlalchemy.String,
                           primary_key=True)

    payer_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    amount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String)

