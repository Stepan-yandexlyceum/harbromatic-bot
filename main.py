from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from functions import *


id_user = ''
topics_keyboard = [['Google', 'android'],
                       ['linux', 'php'],
                       ['javascript', 'microsoft'],
                       ['apple', 'социальные сети'],
                       ['стартапы', 'программирование'],
                       ['Apple', 'дизайн'],
                       ['python', 'юмор'],
                       ['интернет', 'хабрахабр']]


def start(update, content):
    global id_user
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
    user_topics.append(update.message.text)


def set_authors(update, context):
    update.message.reply_text("Возможно, ты хотел бы видеть посты конкретных авторов. Если же нет, введи /skip")
    if update.message.text == "/skip":
        return 3
    else:
        user_authors.append(update.message.text)
    
def get_my_topics(update, context):
    topics = get_topic(id_user)

    if topics == 'None':
        update.message.reply_text('Похоже у вас еще нет избранных тем')
    update.message.reply_text(', '.join(topics))

                            
def accepting_response(update, context):
    
    answer = update.message.text
    add_topic(id_user, answer)



def stop(update, context):
    pass


def main():
    updater = Updater('1763812353:AAGFHoh-fKzDAj4oOX_CR_QW7wMZGDjAML0', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(Filters.text, set_topics)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(Filters.text, set_authors)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    conv_handler_topics = ConversationHandler(
        entry_points=[CommandHandler('set_topics', set_topics)],
        states={
            # Функция читает ответ на вопрос.
            1: [MessageHandler(Filters.text, accepting_response)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop_topics', stop)]
    )

    dp.add_handler(conv_handler_topics)

    # text_handler = MessageHandler(Filters.text, echo)
    # dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set_topics", set_topics))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
