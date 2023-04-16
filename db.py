import sqlite3

def start():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    company_name TEXT,
    model_name TEXT,
    price INTEGER);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER
    balance INTEGER
    basket TEXT);''')
    cur.execute('''CREATE TABLE IF NOT EXISTS payments(
    bill_id TEXT,
    payer_id INTEGER,
    amount INTEGER,
    status TEXT);''')
    conn.commit()


def add_product(company_name, model_name, price):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f'''INSERT INTO products(company_name, model_name, price) VALUES ('{company_name}', '{model_name}', '{price});''')
    conn.commit()


def get_product_by_id(product_id):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM products WHERE product_id = {product_id};''')
    data = cur.fetchall()[0]
    return data


def create_user(user_id):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f'''SELECT * FROM users WHERE user_id = {user_id}''')
    if cur.fetchall():
        return
    cur.execute(f'''INSERT INTO users(user_id, balance, basket) VALUES ({user_id}, 0, '');''')
    conn.commit()

def get_company_names(company_name):
    pass