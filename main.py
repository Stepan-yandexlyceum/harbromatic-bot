from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from functions import *


def start(update, content):
    id_user = update.message.chat.id
    name = update.message.chat.first_name
    if is_new_user(id_user):
        add_user(id_user)
        
    update.message.reply_text("Привет! Похоже, ты впервые пользуешься этим ботом. Для того, чтобы узнать,"
                              " что он умеет, введи команду /help")
    return 1


def help(update, context):
    update.message.reply_text(
        "Я - бот для оповещения о новых постах на habr.com Ты можешь рассказать мне, какие темы тебя интересуют и"
        " я помогу тебе не пропустить ни один пост по данным темам")


def set_topics(update, context):
    topics_keyboard = [['Google', 'android'],
                       ['linux', 'php'],
                       ['javascript', 'microsoft'],
                       ['apple', 'социальные сети'],
                       ['стартапы', 'программирование'],
                       ['Apple', 'дизайн'],
                       ['python', 'юмор'],
                       ['интернет', 'хабрахабр']]
    markup = ReplyKeyboardMarkup(topics_keyboard, one_time_keyboard=False)
    reply_markup = markup
    update.message.reply_text("Расскажи мне о своих интересах, чтобы я мог подобрать для тебя интересные статьи",
                              reply_markup=markup)


def stop(update, context):
    pass


def main():
    updater = Updater('1768048648:AAFgaWJzCEkpQGp4Lt4401O53se7ePNEAsU', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text, set_topics)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text, set_topics)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    # text_handler = MessageHandler(Filters.text, echo)
    # dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set_topics", set_topics))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
