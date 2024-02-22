import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import requests
import config
import datetime
from messages import START_MSG_1, START_MSG_2, LESSON_MSG, CHECK_FAIL_MSG, SUCCESS_MSG

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    btn_1 = InlineKeyboardButton('Получить урок', callback_data="btn_start")
    keyboard_markup.add(btn_1)
    
    with open('static/1.jpg', 'rb') as img:    
        bot.send_photo(message.from_user.id, img, START_MSG_1, parse_mode='HTML')
        bot.send_message(message.from_user.id, START_MSG_2, reply_markup=keyboard_markup)

def get_markup():
    keyboard_markup = InlineKeyboardMarkup(row_width=2)
    btn_1 = InlineKeyboardButton('Получить урок', callback_data="btn_get_lesson")
    btn_2 = InlineKeyboardButton('Подписаться', url= "https://t.me/prvms_test", callback_data="btn_subscribe")
    keyboard_markup.add(btn_1, btn_2)
        
    return keyboard_markup

def send_video(chat_id):
    url = '{api_url}/bot{token}/sendvideo'.format(token=config.TELEGRAM_TOKEN, api_url=config.API_URL)
    resp = requests.post(url, data={'chat_id': chat_id, 'video': config.LESSON_VIDEO_ID, 'supports_streaming': True, 'width': 1686, 'height': 1080})
    
def get_video_id(chat_id):
    with open('static/lesson.mov', 'rb') as video:
        url = '{api_url}/bot{token}/sendvideo'.format(token=config.TELEGRAM_TOKEN, api_url=config.API_URL)
        resp = requests.post(url, data={'chat_id': chat_id,'supports_streaming': True, 'width': 1686, 'height': 1080}, files={'video': video})
        print(resp.json()['result']['video']['file_id'])
        return resp.json()['result']['video']['file_id']

@bot.callback_query_handler(func=lambda call: True)
def get_answer(call):
    if call.data == "btn_start":
        with open('static/2.jpg', 'rb') as img:
            bot.send_photo(call.from_user.id, img, LESSON_MSG, reply_markup=get_markup())
    
    elif call.data == "btn_get_lesson":
        user = bot.get_chat_member(config.TARGET_CHANNEL_ID, call.from_user.id)
        
        if user.status in ['member', 'administrator', 'creator']:
            with open('static/3.jpg', 'rb') as img:
                bot.send_photo(call.from_user.id, img, SUCCESS_MSG)
            send_video(call.from_user.id)
            #id = get_video_id(call.from_user.id)
            #print(id)
            
        else:
            bot.send_message(call.from_user.id, CHECK_FAIL_MSG, reply_markup=get_markup())
        
bot.infinity_polling(logger_level=logging.DEBUG)