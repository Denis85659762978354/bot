import telebot
from telebot import types

bot = telebot.TeleBot('5994112406:AAHIWj1rdeSiVSijLxuMMwpQKzy1UwZaJEg')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Hello, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Hello':
        bot.send_message(message.chat.id, "Hello!", parse_mode='html')
    elif message.text == 'id':
        bot.send_message(message.chat.id, f"Your ID: {message.from_user.id}", parse_mode='html')
    elif message.text == 'photo':
        photo = open('photo1.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    else:
        bot.send_message(message.chat.id, "I don't understand you", parse_mode='html')

@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Good photo')

@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Go to Website', url="https://www.pythonanywhere.com"))
    bot.send_message(message.chat.id, 'Go to site', reply_markup=markup)

bot.polling(none_stop=True)
