import telebot
from telebot import types
import db


bot = telebot.TeleBot('5923980996:AAF_jL5eHv0gIHC98-_p2LTP-wQ8gzXTPrA')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Товары", callback_data='show_products')
    btn2 = types.InlineKeyboardButton("Корзина", callback_data='show_basket')
    btn3 = types.InlineKeyboardButton("Пополнить баланс", callback_data='get_money')
    markup.row(btn1, btn2, btn3)
    bot.reply_to(message, 'Главное меню', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def show_company_products(callback):
    markup = types.InlineKeyboardMarkup()
    for company in company_names:
        markup.add(types.InlineKeyboardButton(text=company, callback_data=f'company_{company}'))
    callback_query.message.answer('Выберите производителя', reply_markup=markup)


@dp.callback_query_handler(lambda query: query.startswith('company_'))
async def show_company_product(callback_query: types.CallbackQuery):
    company = callback_query.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    products = db.get_company_products(company)
    for product in products:
        markup.add(types.InlineKeyboardButton(text=product[1], callback_data=f'show_id_{product[0]}'))
    markup.add(types.InlineKeyboardButton(text='Назад', callback_data='show_products'))



bot.infinity_polling()
