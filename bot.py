import telebot
from telebot import types


bot = telebot.TeleBot('5923980996:AAF_jL5eHv0gIHC98-_p2LTP-wQ8gzXTPrA')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Товары", callback_data='products')
    btn2 = types.InlineKeyboardButton("Корзина", callback_data='basket')
    btn3 = types.InlineKeyboardButton("Пополнить баланс", callback_data='get_money')
    markup.row(btn1, btn2, btn3)
    bot.reply_to(message, 'Главное меню', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def show_products(callback):
    if callback.data == 'products':
        bot.reply_to(callback.message, "Выберите производителя")
    elif callback.data == 'basket':
        bot.reply_to(callback.message, 'Вы нажали на кнопку Корзина')
    elif callback.data == 'get_money':
        bot.reply_to(callback.message, 'Вы нажали на кнопку Пополнить баланс')


bot.infinity_polling()
