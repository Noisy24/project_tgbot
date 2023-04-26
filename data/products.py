import sqlalchemy
from data.db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    product_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)

    company_name = sqlalchemy.Column(sqlalchemy.String)
    model_name = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)
