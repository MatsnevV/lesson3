"""1
 Научите бота играть в города. Правила такие - внутри бота есть список городов, 
 пользователь пишет /cities Москва и если в списке такой город есть,
  бот отвечает городом на букву "а" - "Альметьевск, ваш ход". 
  Оба города должны удаляться из списка.

    Помните, с ботом могут играть несколько пользователей одновременно

2 
 Научите бота выполнять основные арифметические действия с двумя числами: сложение, вычитание,
  умножение и деление. Если боту дать команду /calc 2-3, он должен ответить “-1”.

    Не забудьте обработать возможные ошибки во вводе: пробелы, отсутствие чисел, деление на ноль
    Подумайте, как можно сделать поддержку действий с тремя и более числами

3
 Реализуйте в боте команду /wordcount которая считает слова в присланной фразе.
Например на запрос /wordcount Привет как дела бот должен ответить: 3 слова.
Не забудьте:

    Добавить проверки на пустую строку
    Как можно обмануть бота, какие еще проверки нужны?

4
Реализуйте в боте команду, которая отвечает на вопрос 
“Когда ближайшее полнолуние?” Например /next_full_moon 2019-01-01. 
Чтобы узнать, когда ближайшее полнолуние, используйте ephem.next_full_moon(ДАТА) 

"""
#
from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler


import settings #настройка прокси и API


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = f'Привет {emo}'
    update.message.reply_text(text, reply_markup=get_keyboard())

def greet_user_first(bot, update):
    text = 'Вызван /start'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f'Привет {update.message.chat.first_name}{emo}!\nТы написал:{update.message.text}'
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, 
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id, photo=open(
        cat_pic, 'rd'), reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
        emo = get_user_emo(user_data)
        update.message.reply_text(
            f'Готово: {emo}', reply_markup=get_keyboard())


def get_contact(bot, message, user_data):
    print(update.message.contact)
    update.message.reply_text(
        f'Готово: {get_user_emo(user_data)}', reply_markup=get_keyboard())


def get_location(bot, message, user_data):
    print(update.message.location)
    update.message.reply_text(
        f'Готово: {get_user_emo(user_data)}', reply_markup=get_keyboard())

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(
            choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def get_keyboard():
    contact_botton = KeyboardButton('прислать  контакты', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика', 'Сменить аватарку'],
                                        [contact_botton, location_button]
                                        ], resize_keyboard=True
                                        )
    return my_keyboard
def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info('бот запускается')
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler(
        "start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler(
        "cat", send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^ (Сменить аватарку)$', change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact,
                                  get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location,
                              get_location, pass_user_data=True))

    dp.add_handler(MessageHandler(
        Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()


#if __name__ == '__main__':
#    main()
main()
