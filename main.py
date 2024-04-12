import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import requests
import config
import datetime
from messages import START_MSG_1, START_MSG_2, LESSON_MSG, CHECK_FAIL_MSG, SUCCESS_MSG, BROADCAST_MSG
#from models import User

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

@bot.callback_query_handler(func=lambda call: True)
def get_answer(call):
    print('call data is ', call.data)
    if call.data == "btn_next":
        with open('static/2.jpg', 'rb') as img:
            bot.send_photo(call.from_user.id, img, LESSON_MSG, parse_mode='HTML', reply_markup=get_markup())
    
    if call.data == "btn_start":    
        keyboard_markup = InlineKeyboardMarkup(row_width=1)
        btn_1 = InlineKeyboardButton('Получить урок', callback_data="btn_next")
        keyboard_markup.add(btn_1)
        bot.send_message(call.from_user.id, START_MSG_2, parse_mode='HTML', reply_markup=keyboard_markup)
    
    elif call.data == "btn_get_lesson":
        user = bot.get_chat_member(config.TARGET_CHANNEL_ID, call.from_user.id)
        
        if user.status in ['member', 'administrator', 'creator']:
            with open('static/3.jpg', 'rb') as img:
                bot.send_photo(call.from_user.id, img, SUCCESS_MSG, parse_mode='HTML')
            send_video(call.from_user.id)
            #id = get_video_id(call.from_user.id)
            #print(id)
            
        else:
            bot.send_message(call.from_user.id, CHECK_FAIL_MSG, parse_mode='HTML', reply_markup=get_markup())

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    btn_1 = InlineKeyboardButton('Хочу узнать подробнее', callback_data="btn_start")
    keyboard_markup.add(btn_1)
    #user, is_new = User.get_or_create(telegram_id = message.from_user.id)
    with open('static/1.jpg', 'rb') as img:    
        bot.send_photo(message.from_user.id, img, START_MSG_1, parse_mode='HTML', reply_markup=keyboard_markup)
        #bot.send_message(message.from_user.id, START_MSG_2, reply_markup=keyboard_markup)

@bot.message_handler(commands=[config.BROADCAST_CMD])
def cmd_broadcast(message):
    keyboard_markup = InlineKeyboardMarkup(row_width=1)
    btn_1 = InlineKeyboardButton('ПОДАРОК 🔢', url= 'https://t.me/alexnum_bot')
    keyboard_markup.add(btn_1)
    
    #with open('static/1.jpg', 'rb') as img:    
    #    bot.send_photo(config.TARGET_CHANNEL_ID, img, BROADCAST_MSG, parse_mode='HTML', reply_markup=keyboard_markup)
    
    bot.send_message(config.TARGET_CHANNEL_ID, BROADCAST_MSG, parse_mode='HTML', reply_markup=keyboard_markup)

def get_markup():
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    btn_1 = InlineKeyboardButton('Получить урок', callback_data="btn_get_lesson")
    btn_2 = InlineKeyboardButton('Подписаться', url= config.TARGET_CHANNEL_URL, callback_data="btn_subscribe")
    keyboard_markup.add(btn_1, btn_2)
        
    return keyboard_markup

def send_video(chat_id):
    url = '{api_url}/bot{token}/sendvideo'.format(token=config.TELEGRAM_TOKEN, api_url=config.API_URL)
    resp = requests.post(url, data={'chat_id': chat_id, 'video': config.LESSON_VIDEO_ID, 'supports_streaming': True, 'width': 1686, 'height': 1080, 'protect_content': True})
    
def get_video_id(chat_id):
    with open('static/lesson.mov', 'rb') as video:
        url = '{api_url}/bot{token}/sendvideo'.format(token=config.TELEGRAM_TOKEN, api_url=config.API_URL)
        resp = requests.post(url, data={'chat_id': chat_id,'supports_streaming': True, 'width': 1686, 'height': 1080}, files={'video': video})
        print(resp.json()['result']['video']['file_id'])
        return resp.json()['result']['video']['file_id']



bot.infinity_polling()