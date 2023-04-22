import sqlite3


def start():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    company_name TEXT,
    model_name TEXT,
    price INTEGER);''')
    cur.execute('''CREATE TABLE users(
    user_id INTEGER,
    balance INTEGER,
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
    cur.execute(f'''INSERT INTO products(company_name, model_name, price) VALUES ('{company_name}', '{model_name}', '{price}');''')
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


def get_company_names():
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT company_name FROM products")
    l = set()
    data = cur.fetchall()
    for row in data:
        for x in row:
            l.add(x)
    return l


def get_company_products(company_name):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM products WHERE company_name = '{company_name}'")
    data = cur.fetchall()
    return data


def clean_basket(user_id):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f'''UPDATE users SET basket = '' WHERE user_id = {user_id}''')
    conn.commit()



def create_basket_txt(user_id):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f"SELECT basket FROM users WHERE user_id = {user_id};")
    basket = cur.fetchone()[0]
    with open(f"{user_id}_basket.txt", "w") as f:
        f.write(basket)


def get_user(user_id):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE user_id = {user_id};")
    data = cur.fetchone()
    return data


def add_product_to_basket(user_id, product_id):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f"SELECT basket FROM users WHERE user_id = {user_id};")
    basket = cur.fetchone()[0]
    product = get_product_by_id(product_id)
    if product:
        if basket:
            basket += f",{product_id}"
        else:
            basket = str(product_id)
        cur.execute(f"UPDATE users SET basket = {basket} WHERE user_id = {user_id};")
        conn.commit()
        return True
    return False


def spend_balance(user_id, cost):
    conn = sqlite3.connect('main.db')
    cur = conn.cursor()
    cur.execute(f"SELECT balance FROM users WHERE user_id = {user_id};")
    balance = cur.fetchone()[0]
    if balance >= cost:
        new_balance = balance - cost
        cur.execute(f"UPDATE users SET balance = {new_balance} WHERE user_id = {user_id};")
        conn.commit()
        return True
    return False

