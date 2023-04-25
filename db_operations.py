from data import db_session
from data.users import User
from data.payments import Payment
from data.products import Product


def add_product(company_name, model_name, price):
    db_sess = db_session.create_session()
    new_product = Product(company_name=company_name, model_name=model_name, price=price)
    db_sess.add(new_product)
    db_sess.commit()


def get_product_by_id(product_id):
    db_sess = db_session.create_session()
    product = db_sess.query(Product).filter(Product.product_id == product_id).first()
    return product


def create_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    if user is None:
        new_user = User(user_id=user_id, balance=0, basket='')
        db_sess.add(new_user)
        db_sess.commit()


def get_company_names():
    db_sess = db_session.create_session()
    companies = db_sess.query(Product.company_name).distinct().all()
    company_names = set([company[0] for company in companies])
    return company_names


def get_company_products(company_name):
    db_sess = db_session.create_session()
    products = db_sess.query(Product).filter(Product.company_name == company_name).all()
    return products


def clean_basket(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    user.basket = ''
    db_sess.commit()


def create_basket_txt(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    basket = user.basket
    with open(f"{user_id}_basket.txt", "w") as f:
        f.write(basket)


def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    return user


def add_product_to_basket(user_id, product_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    product = get_product_by_id(product_id)
    if product:
        if user.basket:
            user.basket += f",{product_id}"
        else:
            user.basket = str(product_id)
        db_sess.commit()
        return True
    return False


def spend_balance(user_id, cost):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.user_id == user_id).first()
    if user.balance >= cost:
        user.balance -= cost
        db_sess.commit()
        return True
    return False


