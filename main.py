from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from functions import *
from telegram import ReplyKeyboardRemove


def start(update, content):
    global id_user
    id_user = update.message.chat.id
    
    name = update.message.chat.first_name
    if is_new_user(id_user):
        add_user(id_user)

    update.message.reply_text("Привет! Похоже, ты впервые пользуешься этим ботом. Для того, чтобы узнать,"
                              " что он умеет, введи команду /help. Чтобы выбрать темы, по которым будет производиться"
                              " оповещение, введи /set_specialization")
    return 1


def help(update, context):
    update.message.reply_text(
        "Я - бот для оповещения о новых вакансиях на hh.ru Ты можешь рассказать мне, какие профессии и цены тебя интересуют и"
        " я помогу тебе не пропустить ни одну вакансию")


def set_specialization(update, context):
    if update.message.text == "/accept":
        update.message.reply_text(
            "Введите свою специальность",
            reply_markup=ReplyKeyboardRemove())
        return 3
    else:
        user_topics.append(update.message.text)
        return 2


def set_topics2(update, context):
    if update.message.text == "/accept":
        update.message.reply_text(
            "Возможно, ты хотел бы видеть посты конкретных авторов. Для подтверждения или если же нет, введи /accept",
            reply_markup=ReplyKeyboardRemove())
        return 3
    else:
        user_topics.append(update.message.text)
        return 2


def set_data(update, context):
    if update.message.text == "/accept":
        update.message.reply_text("Итак, я оповещу тебя по следующим темам:")
        for i in user_topics:
            update.message.reply_text(i)
        if user_authors:
            update.message.reply_text("А также о публикациях следующих авторов:")
            for i in user_authors:
                update.message.reply_text(i)
        return 4
    else:
        user_authors.append(update.message.text)
        return 3


def get_my_topics(update, context):
    topics = get_topic(id_user)

    if topics == 'None':
        update.message.reply_text('Похоже у вас еще нет избранных тем')
    update.message.reply_text(', '.join(topics))

                            
def accepting_response(update, context):
    answer = update.message.text
    add_topic(id_user, answer)


def final_set(update, context):
    pass


def stop(update, context):
    pass


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def open_keyboard(update, context):
    topics_keyboard = [['/help', '/set_specialization'],
                       ['/get_my_topics', '/close_keyboard']]
    markup = ReplyKeyboardMarkup(topics_keyboard, one_time_keyboard=False)
    update.message.reply_text(
        "Ok",
        reply_markup=markup
    )


def main():
    updater = Updater('1768048648:AAFgaWJzCEkpQGp4Lt4401O53se7ePNEAsU', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, set_topics, pass_user_data=True)],
            2: [MessageHandler(Filters.text, set_topics2, pass_user_data=True)],
            3: [MessageHandler(Filters.text, set_authors, pass_user_data=True)],
            4: [MessageHandler(Filters.text, final_set, pass_user_data=True)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    # text_handler = MessageHandler(Filters.text, echo)
    # dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("set_topics", set_specialization))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
