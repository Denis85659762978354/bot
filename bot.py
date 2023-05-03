
import telebot
from currency_converter import  CurrencyConverter
from telebot import types

bot = telebot.TeleBot('5994112406:AAHIWj1rdeSiVSijLxuMMwpQKzy1UwZaJEg')
currency =  CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hello, <b>{message.from_user.first_name} </b>, Enter amount:'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.register_next_step_handler(message, summa)

@bot.message_handler(commands=['help'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
    website = types.KeyboardButton('/website')
    start = types.KeyboardButton('/start')
    help = types.KeyboardButton('/help')
    markup.add(website, start, help)
    bot.send_message(message.chat.id, 'You can go to site /website', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Come out: {round(res, 2)}. You can re-enter the amount')
        bot.register_next_step_handler(call.message, summa)
    else:
        if call.data == 'help':
            website(call.message)
        else:
            bot.send_message(call.message.chat.id, 'Enter a pair of values via / ')
            bot.register_next_step_handler(call.message, my_currency)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid fotmat enter amount')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width = 2)
        b1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        b2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        b3 = types.InlineKeyboardButton('PLN/USD', callback_data='pln/usd')
        b4 = types.InlineKeyboardButton('GBP/USD', callback_data='gbp/usd')
        b5 = types.InlineKeyboardButton('USD/PLN', callback_data='usd/pln')
        b6 = types.InlineKeyboardButton('Another', callback_data='else')
        markup.add(b1, b2, b3, b4, b5, b6)
        bot.send_message(message.chat.id, 'Select currency pair, If you need help click : /help ', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, 'Number must be greated then 0')
        bot.register_next_step_handler(message, summa)


def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Come out: {round(res, 2)}. You can re-enter the amount')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f'Something is wrong, enter the meaning again')
        bot.register_next_step_handler(message, my_currency)

@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Go to Website', url="https://www.xe.com/currencyconverter"))
    bot.send_message(message.chat.id, 'Currency Converter', reply_markup=markup)

bot.polling(none_stop=True)
