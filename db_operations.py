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
    return [product.product_id, product.company_name, product.model_name, product.price]



def create_user(users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == users_id).first()
    if user is None:
        new_user = User(users_id=users_id, balance=0, basket='')
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
    result = [[product.product_id, product.company_name, product.model_name, product.price] for product in products]
    print(result)
    return result


def clean_basket(users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == users_id).first()
    user.basket = ''
    db_sess.commit()


def create_basket_txt(users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == users_id).first()
    basket = str(user.basket)
    with open(f"{users_id}_basket.txt", "w") as f:
        f.write(basket)
    return basket


def get_user(users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == users_id).first()
    if user:
        return [user.users_id, user.balance, user.basket]
    return []


def add_product_to_basket(product_id, users_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == users_id).first()
    product = get_product_by_id(product_id)
    if product:
        basket = user.basket.split(';')
        basket.append(str(product_id))
        user.basket = ';'.join(basket)
        db_sess.commit()
        return True
    return False


def spend_balance(users_id, cost):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == users_id).first()
    if user.balance >= cost:
        user.balance -= cost
        db_sess.commit()
        return True
    return False


