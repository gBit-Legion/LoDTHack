import requests
import datetime
from random import randrange

import telebot
from telebot import types
from loguru import logger

TOKEN = "5821613520:AAFM7de1mQvJg1T6HiMskQe72JhS_icoBL8"
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


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Мы рады приветствовать Вас!!! "
                                      "Ваш заказ №_______ "
                                      "Ожидает получения по адресу:______ "
                                      "Забирите его до: дд.мм.гггг Код получения: х-х-х-х.  ")
    return ()


# Сообщение по факту получения
@bot.message_handler(commands=['received'])
def received(message):
    markup = types.InlineKeyboardMarkup(row_width=5)
    button1 = types.InlineKeyboardButton('1', callback_data="1")
    button2 = types.InlineKeyboardButton('2', callback_data="2")
    button3 = types.InlineKeyboardButton('3', callback_data="3")
    button4 = types.InlineKeyboardButton('4', callback_data="4")
    button5 = types.InlineKeyboardButton('5', callback_data="5")

    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, " Вы получили заказ! Спасибо, что выбрали именно нас. "
                                      "Оцените пожалуйста работу нашего сервиса и качество доставки от 1 до 5 - это "
                                      "поможет нам стать лучше. ",
                     reply_markup=markup)
    return ()


# Нажали на кнопку 1
@bot.callback_query_handler(func=lambda call1: call1.data == "1")
def answr(call1):
    answr1 = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Да', callback_data="yes")
    no = types.InlineKeyboardButton('Нет, спасибо', callback_data="no")
    answr1.add(yes, no)
    bot.send_message(call1.from_user.id, " Хотите оставить небольшой отзыв? Ваше мнение важно для нас.",
                     reply_markup=answr1)
    bot.answer_callback_query(callback_query_id=call1.id)
    mark = 1
    logger.debug(mark)
    # продолжение оставления отзыва
    @bot.callback_query_handler(func=lambda callback_obj1: True)
    def callback_function1(callback_obj1):
        if callback_obj1.data == "yes":
            bot.send_message(callback_obj1.from_user.id, "Напишите свой отзыв и отправьте мне, я его передам.")
            # Ответ бота на любое написанное сообщение.
            @bot.message_handler(func=lambda message1: True)
            def answr111(message1):
                bot.reply_to(message1, "Спасибо, что оставили отзыв!")
                bot.answer_callback_query(callback_query_id=callback_obj1.id)
                # сбор инфы о пользователе, текста сообщения
                usertext = message1.text
                logger.debug(usertext)
                # Отсылаем на бэк отзыв (класс не определен, определена оценка)
                sendReview(mark, usertext, str(-999))
            return ()
        elif callback_obj1.data == "no":
            bot.send_message(callback_obj1.from_user.id, "Спасибо, что использовали наш сервис, до новых встреч!")
            bot.answer_callback_query(callback_query_id=callback_obj1.id)
            reviewdata = datetime.datetime.fromtimestamp(callback_obj1.date)
            print(reviewdata.strftime('%Y-%m-%d %H:%M:%S'))

        bot.answer_callback_query(callback_query_id=callback_obj1.id)
        return ()
    return ()


# Нажали на кнопку 2
@bot.callback_query_handler(func=lambda call2: call2.data == "2")
def answr(call2):
    answr222 = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Да', callback_data="yes")
    no = types.InlineKeyboardButton('Нет, спасибо', callback_data="no")
    answr222.add(yes, no)
    bot.send_message(call2.from_user.id, " Хотите оставить небольшой отзыв? Ваше мнение важно для нас.",
                     reply_markup=answr222)
    bot.answer_callback_query(callback_query_id=call2.id)
    mark = 2
    print(mark)
    # продолжение оставления отзыва
    @bot.callback_query_handler(func=lambda callback_obj2: True)
    def callback_function1(callback_obj2):
        if callback_obj2.data == "yes":
            bot.send_message(callback_obj2.from_user.id, "Напишите свой отзыв и отправьте мне, я его передам.")
            # Ответ бота на любое написанное сообщение.
            @bot.message_handler(func=lambda message2: True)
            def answr1(message2):
                bot.reply_to(message2, "Спасибо, что оставили отзыв!")
                bot.answer_callback_query(callback_query_id=callback_obj2.id)
                # сбор инфы о пользователе, текста сообщения
                usertext = message2.text
                logger.debug(usertext)
                sendReview(mark, usertext, str(-999))
            return ()
        elif callback_obj2.data == "no":
            bot.send_message(callback_obj2.from_user.id, "Спасибо, что использовали наш сервис, до новых встреч!")
            bot.answer_callback_query(callback_query_id=callback_obj2.id)
        bot.answer_callback_query(callback_query_id=callback_obj2.id)
        return ()
    return ()


# Нажали на кнопку 3
@bot.callback_query_handler(func=lambda call3: call3.data == "3")
def answr(call3):
    answr333 = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Да', callback_data="yes")
    no = types.InlineKeyboardButton('Нет, спасибо', callback_data="no")
    answr333.add(yes, no)
    bot.send_message(call3.from_user.id, " Хотите оставить небольшой отзыв? Ваше мнение важно для нас.",
                     reply_markup=answr333)
    bot.answer_callback_query(callback_query_id=call3.id)
    mark = 3
    logger.debug(mark)

    # продолжение оставления отзыва
    @bot.callback_query_handler(func=lambda callback_obj3: True)
    def callback_function1(callback_obj3):
        if callback_obj3.data == "yes":
            bot.send_message(callback_obj3.from_user.id, "Напишите свой отзыв и отправьте мне, я его передам.")
            # Ответ бота на любое написанное сообщение.
            @bot.message_handler(func=lambda message3: True)
            def answr1(message3):
                bot.reply_to(message3, "Спасибо, что оставили отзыв!")
                bot.answer_callback_query(callback_query_id=callback_obj3.id)
                # сбор инфы о пользователе, текста сообщения
                usertext = message3.text
                logger.debug(usertext)
                sendReview(mark, usertext, str(-999))
            return ()
        elif callback_obj3.data == "no":
            bot.send_message(callback_obj3.from_user.id, "Спасибо, что использовали наш сервис, до новых встреч!")
            bot.answer_callback_query(callback_query_id=callback_obj3.id)
        return ()

    return ()


# Нажали на кнопку 4
@bot.callback_query_handler(func=lambda call4: call4.data == "4")
def answr444(call4):
    answr444 = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Да', callback_data="yes")
    no = types.InlineKeyboardButton('Нет, спасибо', callback_data="no")
    answr444.add(yes, no)
    bot.send_message(call4.from_user.id, " Хотите оставить небольшой отзыв? Ваше мнение важно для нас.",
                     reply_markup=answr444)
    bot.answer_callback_query(callback_query_id=call4.id)
    mark = 4
    logger.debug(mark)
    # продолжение оставления отзыва
    @bot.callback_query_handler(func=lambda callback_obj4: True)
    def callback_function1(callback_obj4):
        if callback_obj4.data == "yes":
            bot.send_message(callback_obj4.from_user.id, "Напишите свой отзыв и отправьте мне, я его передам.")
            # Ответ бота на любое написанное сообщение.
            @bot.message_handler(func=lambda message4: True)
            def answr1(message4):
                bot.reply_to(message4, "Спасибо, что оставили отзыв!")
                bot.answer_callback_query(callback_query_id=callback_obj4.id)
                # сбор инфы о пользователе, текста сообщения
                usertext = message4.text
                logger.debug(usertext)
                sendReview(mark, usertext, str(-999))
            return ()
        elif callback_obj4.data == "no":
            bot.send_message(callback_obj4.from_user.id, "Спасибо, что использовали наш сервис, до новых встреч!")
            bot.answer_callback_query(callback_query_id=callback_obj4.id)
        return ()
    return ()


# Нажали на кнопку 5
@bot.callback_query_handler(func=lambda call5: call5.data == "5")
def answr555(call5):
    answr555 = types.InlineKeyboardMarkup(row_width=2)
    yes = types.InlineKeyboardButton('Да', callback_data="yes")
    no = types.InlineKeyboardButton('Нет, спасибо', callback_data="no")
    answr555.add(yes, no)
    bot.send_message(call5.from_user.id, " Хотите оставить небольшой отзыв? Ваше мнение важно для нас.",
                     reply_markup=answr555)
    bot.answer_callback_query(callback_query_id=call5.id)
    mark = 5
    logger.debug(mark)

    # продолжение оставления отзыва
    @bot.callback_query_handler(func=lambda callback_obj5: True)
    def callback_function1(callback_obj5):
        if callback_obj5.data == "yes":
            bot.send_message(callback_obj5.from_user.id, "Напишите свой отзыв и отправьте мне, я его передам.")
            # Ответ бота на любое написанное сообщение.
            @bot.message_handler(func=lambda message5: True)
            def answr1(message5):
                bot.reply_to(message5, "Спасибо, что оставили отзыв!")
                bot.answer_callback_query(callback_query_id=callback_obj5.id)
                # сбор инфы о пользователе, текста сообщения
                usertext = message5.text
                logger.debug(usertext)
                sendReview(mark, usertext, str(-999))

            return ()
        elif callback_obj5.data == "no":
            bot.send_message(callback_obj5.from_user.id, "Спасибо, что использовали наш сервис, до новых встреч!")
            bot.answer_callback_query(callback_query_id=callback_obj5.id)
        return ()
    return ()

"""
#реализация взаимодействия по команде help
@bot.message_handler(commands=['help'])
def help(cmd_help):
    mark = 1.0

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

 #нажали на кнопку "проблемы с товаром" 1
@bot.callback_query_handler(func=lambda call_help11: call_help11.data == "11")
def answr2(call_help11):
    mark = 1.0
    bot.send_message(call_help11.from_user.id, "Подробно опишите возникшую проблему")

    @bot.message_handler(func=lambda send_admin11: True)
    def send_admin(send_admin11):
        bot.reply_to(send_admin11, "Я передал Вашу жалобу")
        # ТОЛМАС - тренируйся
        text_help = send_admin11.text
        logger.debug(text_help)
        sendReview(mark, usertext=text_help, classnumber=1)
        bot.answer_callback_query(callback_query_id=call_help11.id)
        return()
    return ()
 #нажали на кнопку"Возникли проблемы с курьером" 2
@bot.callback_query_handler(func=lambda call_help12: call_help12.data == "12")
def answr2(call_help12):
    mark = 1.0
    bot.send_message(call_help12.from_user.id, "Подробно опишите возникшую проблему")
    bot.answer_callback_query(callback_query_id=call_help12.id)
    @bot.message_handler(func=lambda send_admin12: True)
    def send_admin(send_admin12):
        bot.send_message(send_admin12.chat.id, "Я передал Вашу жалобу")
        # ТОЛМАС!
        text_help = send_admin12.text
        logger.debug(text_help)
        sendReview(mark, usertext=text_help, classnumber=2)
        bot.answer_callback_query(callback_query_id=call_help12.id)
        return ()
    return ()

 #нажали на кнопку"Проблемы с постаматом" 3
@bot.callback_query_handler(func=lambda call_help13: call_help13.data == "13")
def answr2(call_help13):
    mark = 1.0
    bot.send_message(call_help13.from_user.id, "Подробно опишите возникшую проблему")

    @bot.message_handler(func=lambda send_admin13: True)
    def send_admin(send_admin13):
        bot.send_message(send_admin13.chat.id, "Я передал Вашу жалобу")
        # ТОЛМАС
        text_help = send_admin13.text
        logger.debug(text_help)
        sendReview(mark, usertext=text_help, classnumber=3)
        bot.answer_callback_query(callback_query_id=call_help13.id)
        return ()
    return ()

 #нажали на кнопку"Долго не приходит посылка" 4
@bot.callback_query_handler(func=lambda call_help14: call_help14.data == "14")
def answr2(call_help14):
    mark = 1.0
    bot.send_message(call_help14.from_user.id, "Подробно опишите возникшую проблему")

    @bot.message_handler(func=lambda send_admin14: True)
    def send_admin(send_admin14):
        bot.send_message(send_admin14.chat.id, "Я передал Вашу жалобу")
        # ТОЛМАС
        text_help = send_admin14.text
        logger.debug(text_help)
        sendReview(mark, usertext=text_help, classnumber=4)
        bot.answer_callback_query(callback_query_id=call_help14.id)
        return ()
    return ()

 #нажали на кнопку"ошибся все хорошо" 0
@bot.callback_query_handler(func=lambda call_help15: call_help15.data == "15")
def answr2(call_help15):
    mark = 1.0
    bot.send_message(call_help15.from_user.id, "Подробно опишите возникшую проблему")
    bot.answer_callback_query(callback_query_id=call_help15.id)
    @bot.message_handler(func=lambda send_admin15: True)
    def send_admin(send_admin15):
        bot.send_message(send_admin15.chat.id, "Я передал Вашу жалобу")
        # ТОЛМАС (здесь класс 0)
        text_help = send_admin15.text
        logger.debug(text_help)
        sendReview(mark, usertext=text_help, classnumber=0)
        bot.answer_callback_query(callback_query_id=call_help15.id)
        return ()

    return ()
"""

bot.polling(none_stop=True, interval=0)
