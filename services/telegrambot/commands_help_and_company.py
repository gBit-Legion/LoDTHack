import requests
import datetime
from random import randrange

import telebot
from telebot import types
from loguru import logger

TOKEN = '5833939210:AAGqM9WBBxQPtzNQddyPTPzbpCRF3WUEtZg'
bot = telebot.TeleBot(TOKEN)
logger.success('Telegram bot started!')


def sendReview(mark, usertext, classnumber):
 reviewdata = datetime.datetime.now()
 article = randrange(1, 999999, 1)

 requests.post('http://178.170.196.251:8081/addReview/',
                 json = {
                     "usertext": usertext,
                     "mark": mark,
                     "reviewdate": str(reviewdata),
                     "adress": "Москва, Садовая-Кудринская ул., 3Б",
                     "clusternumber": -999,
                     "classnumber": classnumber,  #значение нажатой кнопки
                     "article": article,
                     "seller": "YandexMarket(TG bot)",
                     "latitude": 0,
                     "longtude": 0,
                 }
             )



@bot.message_handler(commands=['help'])
def help_command(cmd_help):
    #mark = 1.0
    mrkp = types.InlineKeyboardMarkup(row_width=1)
    button01 = types.InlineKeyboardButton('Проблемы с товаром',callback_data='11')
    button02 = types.InlineKeyboardButton('Возникли проблемы с курьером', callback_data='12')
    button03 = types.InlineKeyboardButton('Проблемы с постаматом', callback_data='13')
    button04 = types.InlineKeyboardButton('Долго не приходит посылка', callback_data='14')
    button05 = types.InlineKeyboardButton('Ошибся, все хорошо.', callback_data='15')

    mrkp.add(button01, button02, button03, button04, button05)
    bot.send_message(cmd_help.chat.id, "Если возникли какие-то проблемы или сложности, просто выберите подходящее, "
                                       "мы будем рады Вам помочь",
                     reply_markup=mrkp)
    return ()
@bot.callback_query_handler(func=lambda call_help: True)
def callback_help(call_help):
    if call_help.data == '11':
        bot.send_message(call_help.from_user.id, "Приносим свои извинения, за доставленные неудобства 🥺 "
                                                 "Подробно опишите возникшую проблему с товаром")

        bot.reply_to(call_help, "Я передал Вашу жалобу специалистам, в скором времени это исправят")
        mark = 1.0
        class_number = 1
        text_help = call_help.text
        sendReview(mark, usertext=text_help, classnumber=class_number)

    elif call_help.data == '12':
        bot.send_message(call_help.from_user.id, "Приносим свои извинения, за доставленные неудобства 🥺 "
                                                 "Подробно опишите возникшую проблему с курьером")
        bot.reply_to(call_help, "Я передал Вашу жалобу специалистам, в скором времени это исправят")
        mark = 1.0
        class_number = 2
        text_help = call_help.text
        sendReview(mark, usertext=text_help, classnumber=class_number)

    elif call_help.data == '13':
        bot.send_message(call_help.from_user.id, "Приносим свои извинения, за доставленные неудобства 🥺 "
                                                 "Подробно опишите возникшую проблему с постаматом")
        bot.reply_to(call_help, "Я передал Вашу жалобу специалистам, в скором времени это исправят")
        mark = 1.0
        class_number = 3
        text_help = call_help.text
        sendReview(mark, usertext=text_help, classnumber=class_number)

    elif call_help.data == '14':
        bot.send_message(call_help.from_user.id, "Приносим свои извинения, за доставленные неудобства 🥺 "
                                                 "Подробно опишите возникшую проблему")
        bot.reply_to(call_help, "Я передал Вашу жалобу специалистам, в скором времени это исправят")
        mark = 1.0
        class_number = 4
        text_help = call_help.text
        sendReview(mark, usertext=text_help, classnumber=class_number)

    elif call_help.data == '15':
        bot.send_message(call_help.from_user.id, "Мы рады, когда у наших клиентов все замечательно."
                                                 " Спасибо, что Вы выбрали именно нас, до скорых встреч👋🏻")
        mark = 5
        class_number_from_15 = 0
        sendReview(mark, usertext='Все хорошо', classnumber=class_number_from_15)

    bot.answer_callback_query(callback_query_id=call_help.id)

@bot.message_handler(commands=['company'])
def information_company(info_company):
    bot.send_message(info_company.chat.id, 'Проект «Московский постамат» стал ответом на запрос москвичей '
                                           'в бесконтактной, быстрой и удобной системе доставки, расположенной '
                                           'максимально близко к жителям. Сейчас проект находится в стадии реализации '
                                           'и в будущем нацелен на создание в Москве сети, '
                                           'включающей более 10 000 постаматов.')


bot.polling(none_stop=True, interval=0)

