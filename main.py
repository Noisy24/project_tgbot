import logging
import os

from dotenv import load_dotenv
import config

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

from db_operations import add_product, get_product_by_id, create_user, get_company_names, get_company_products, \
    clean_basket, create_basket_txt, get_user, add_product_to_basket, spend_balance
from data.users import User
from data import db_session

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

db_session.global_init("db/datebase.db")


class States(StatesGroup):
    get_amount = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
    create_user(message.from_user.id)
    markup.add(btn1)
    await message.answer('Добро пожаловать в магазин телефонов, нажмите кнопку для перехода в главное меню',
                         reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'main_menu')
async def main_menu(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Товары', callback_data='show_products')
    btn2 = types.InlineKeyboardButton(text='Корзина', callback_data='show_basket')
    btn3 = types.InlineKeyboardButton(text='Пополнить баланс', callback_data='add_balance')
    btn4 = types.InlineKeyboardButton(text='Поддержка', url=config.admin_link)
    markup.add(btn1, btn2, btn3, btn4)

    await callback_query.message.answer('Главное меню', reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'add_balance')
async def add_balance(callback_query: types.CallbackQuery):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.users_id == message.chat.id).first()
    if user:
        try:
            balance_to_add = int(message.text.split()[1])
            user.balance += balance_to_add
            db_sess.commit()
            await message.reply(
                f"Баланс успешно пополнен на {balance_to_add} рублей. Текущий баланс: {user.balance} рублей.")
        except (IndexError, ValueError):
            await message.reply("Введите сумму для пополнения баланса.")
    else:
        await message.reply("Произошла ошибка. Попробуйте позже.")


@dp.callback_query_handler(lambda query: query.data == 'show_products')
async def show_products(callback_query: types.CallbackQuery):
    company_names = get_company_names()
    markup = types.InlineKeyboardMarkup()
    for company in company_names:
        markup.add(types.InlineKeyboardButton(text=company, callback_data=f'company_{company}'))
    await callback_query.message.answer('Выберите производителя', reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data.startswith('company_'))
async def show_company_products(callback_query: types.CallbackQuery):
    company = callback_query.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    products = get_company_products(company)
    print(get_company_products(company))
    for product in products:
        markup.add(types.InlineKeyboardButton(text=product[2], callback_data=f'show_id_{product[0]}'))
    markup.add(types.InlineKeyboardButton(text='Назад', callback_data='show_product'))
    await callback_query.message.edit_text(text='Выберите товар', reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data.startswith('show_id_'))
async def show_product(callback_query: types.CallbackQuery):
    product_id = callback_query.data.split('_')[2]
    product = get_product_by_id(int(product_id))
    product_id, company_name, model_name, price = product
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_basket_{product_id}'))
    markup.add(types.InlineKeyboardButton(text='Вернуться назад', callback_data=f'company_{company_name}'))
    text = f'''Название модели: {model_name}
Производитель: {company_name}
Цена: {price}'''
    await callback_query.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data.startswith('add_basket_'))
async def add_basket(callback_query: types.CallbackQuery):
    product_id = int(callback_query.data.split('_')[2])
    add_product_to_basket(product_id, callback_query.message.chat.id)
    await callback_query.message.edit_text(text='Продукт успешно добавлен в корзину', reply_markup=None)


@dp.callback_query_handler(lambda query: query.data == 'show_basket')
async def show_basket(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Оплатить корзину', callback_data='buy_basket'))
    markup.add(types.InlineKeyboardButton(text='Очистить корзину', callback_data='clear_basket'))
    markup.add(types.InlineKeyboardButton(text='Назад', callback_data='main_menu'))
    user = get_user(callback_query.message.chat.id)
    print(user)
    balance = user[1]
    basket = user[2]
    cost = 0
    if basket:
        for product_id in basket.split('-'):
            prodct = get_product_by_id(int(product_id))
            price = prodct[3]
            cost += price
    text = f'''Ваш баланс: {balance}
Стоимость корзины: {cost}
Ваша корзина:
'''

    text += basket_txt
    await callback_query.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'clear_basket')
async def clear_basket(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Меню', callback_data='main_menu'))
    clean_basket(callback_query.message.chat.id)
    await callback_query.message.edit_text('Корзина очищена', reply_markup=markup)


@dp.callback_query_handler(lambda query: query.data == 'buy_basket')
async def buy_basket(callback_query: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Меню', callback_data='main_menu'))
    user = get_user(callback_query.message.chat.id)
    balance = user[1]
    basket = user[2]
    if not basket:
        await callback_query.message.edit_text('Корзина пуста', reply_markup=markup)
        return
    cost = 0
    for product_id in basket.split():
        product = get_product_by_id(int(product_id))
        price = product[3]
        cost += price
    if cost > balance:
        await callback_query.message.edit_text('Недостатачно средств на балансе', reply_markup=markup)
        return
    await callback_query.message.edit_text('''Покупка прошла успешно.
Ожидайте сообщение от администратора.''', reply_markup=markup)
    user_link = await callback_query.message.chat.get_url()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Написать покупателю', url=user_link))
    text = f'''Пользователь {callback_query.message.chat.username} оплатил покупку
В заказ входят:'''
    basket_txt = create_basket_txt(callback_query.message.chat.id)
    text += basket_txt
    await bot.send_message(chat_id=config.admin_id, text=text)
    spend_balance(callback_query.message.chat.id, cost)
    clean_basket(callback_query.message.chat.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
