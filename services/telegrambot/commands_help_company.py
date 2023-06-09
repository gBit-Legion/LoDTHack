import telebot
from telebot import types
from loguru import logger

token = 'TOKEN_BOT'
bot = telebot.TeleBot(token)
logger.success('Telegram bot started!')
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
        mark = 1.0
        msg = bot.send_message(call_help.from_user.id, "Подробно опишите возникшую проблему")
        bot.register_next_step_handler(msg, send_admin)
    elif call_help.data == '12':
        mark = 1.0
        msg = bot.send_message(call_help.from_user.id, "Подробно опишите возникшую проблему")
        bot.register_next_step_handler(msg, send_admin)
    elif call_help.data == '13':
        mark = 1.0
        msg = bot.send_message(call_help.from_user.id, "Подробно опишите возникшую проблему")
        bot.register_next_step_handler(msg, send_admin)
    elif call_help.data == '14':
        mark = 1.0
        msg = bot.send_message(call_help.from_user.id, "Подробно опишите возникшую проблему")
        bot.register_next_step_handler(msg, send_admin)
    elif call_help.data == '15':
        mark = 1.0
        bot.send_message(call_help.from_user.id, "Мы рады, что Вы выбрали именно нас, до скорых встреч")


    bot.answer_callback_query(callback_query_id=call_help.id)
def send_admin(send_admin):
    bot.reply_to(send_admin, "Я передал Вашу жалобу специалистам, в скором времени это исправят")
    text_help = send_admin.text
    help_username = send_admin
    print(help_username)
    logger.debug(text_help)

# Реализация команды company
@bot.message_handler(commands=['company'])
def information_company(information):
    bot.send_message(information.chat.id, 'Немного полезной инфромации о компании ...')



bot.polling(none_stop=True, interval=0)