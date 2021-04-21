from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from functions import *
from telegram import ReplyKeyboardRemove
import schedule
from web import getJobs

specialization_user = ""
salary_user = []


def start(update, content):
    global id_user, specialization_user, salary_user
    id_user = update.message.chat.id

    name = update.message.chat.first_name
    if is_new_user(id_user):
        add_user(id_user)

    update.message.reply_text("Привет! Похоже, ты впервые пользуешься этим ботом. Для того, чтобы узнать,"
                              " что он умеет, введи команду /help. Чтобы указать свою специальность, по которой будет производиться"
                              " оповещение, введи /set_specialization")
    return 1


def help(update, context):
    update.message.reply_text(
        "Я - бот для оповещения о новых вакансиях на hh.ru Ты можешь рассказать мне, какие профессии и цены тебя интересуют и"
        " я помогу тебе не пропустить ни одну вакансию")


def set_specialization(update, context):
    update.message.reply_text(
        "Введите свою специальность",
        reply_markup=ReplyKeyboardRemove())
    return 2


def reception_specialization(update, context):
    specialization_user = update.message.text
    update_specialization(id_user, specialization_user)
    update.message.reply_text(
        "Теперь введите в каком диапазоне вы хотите получать зарплату (два числа через дефис)",
        reply_markup=ReplyKeyboardRemove())
    return 3


# def reception_salary(update, context):
#     salary_user = update.message.text
#     salary_user = salary_user.replace(' ', '')
#     salary_user = salary_user.split('-')
#     salary_user[0] = int(salary_user[0])
#     salary_user[1] = int(salary_user[1])
#     update_salary(id_user, salary_user)
#     return 4


def final_set(update, context):
    salary_user = update.message.text
    salary_user = salary_user.replace(' ', '')
    salary_user = salary_user.split('-')
    salary_user[0] = int(salary_user[0])
    salary_user[1] = int(salary_user[1])
    update_salary(id_user, salary_user)
    update.message.reply_text(
        "Отлично! Теперь вы не пропустите ни одну вакансию на профессию {} с зарплатой {} - {}руб".format(
            specialization_user, salary_user[0], salary_user[1]))
    schedule.every(15).minutes.do(get_vacancies)
    while True:
        schedule.run_pending()


def get_vacancies(update, context):
    jobs = getJobs(specialization_user, salary_user)
    update.message.reply_text("Не пропустите новые вакансии!")
    for job in jobs:
        update.message.reply_text("Должность: {}"
                                  "Город: {}"
                                  "Зарплата: {}"
                                  "Опубликовано{}"
                                  "Подробнее{}".format(job["name"], job["city"], job["salary"], job["published_at"],
                                                       jobs["url"]))


def stop(update, context):
    pass


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def open_keyboard(update, context):
    topics_keyboard = [['/help', '/set_specialization'],
                       ['/get_my_topics', '/close']]
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
            1: [MessageHandler(Filters.text, set_specialization, pass_user_data=True)],
            2: [MessageHandler(Filters.text, reception_specialization)],
            3: [MessageHandler(Filters.text, final_set)],
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
    dp.add_handler(CommandHandler("set_specialization", set_specialization))
    dp.add_handler(CommandHandler("open", open_keyboard))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
