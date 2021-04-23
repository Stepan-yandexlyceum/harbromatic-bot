from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from functions import *
from telegram import ReplyKeyboardRemove
import schedule
from schedule import every #, repeat
import time
from web import getJobs

specialization_user = ""
salary_user = []
running = True
page = 0


def start(update, content):
    global id_user, specialization_user, salary_user, running
    running = True
    id_user = update.message.chat.id

    name = update.message.chat.first_name
    if is_new_user(id_user):
        add_user(id_user)

    update.message.reply_text("Привет! Похоже, ты впервые пользуешься этим ботом. Для того, чтобы узнать,"
                              " что он умеет, введи команду /help. Чтобы указать свою специальность,"
                              " по которой будет производиться"
                              " оповещение, введи /set_specialization")
    return 1


def help(update, context):
    update.message.reply_text(
        "Я - бот для оповещения о новых вакансиях на hh.ru Ты можешь рассказать мне,"
        " какие профессии и цены тебя интересуют и"
        " я помогу тебе не пропустить ни одну вакансию."
        " Список доступных комманд:\n/set_specialization\n /set_salary\n /set_update_time\n /stop")


def set_specialization(update, context):
    update.message.reply_text(
        "Введите свою специальность",
        reply_markup=ReplyKeyboardRemove())
    return 2


def reception_specialization(update, context):
    global specialization_user
    specialization_user = update.message.text
    update_specialization(id_user, specialization_user)
    update.message.reply_text(
        "Теперь введите в каком диапазоне вы хотите получать зарплату (два числа через дефис)",
        reply_markup=ReplyKeyboardRemove())
    return 3


def set_update_time(update, context):
    global salary_user
    salary_user = update.message.text
    salary_user = salary_user.replace(' ', '')
    salary_user = salary_user.split('-')
    salary_user[0] = int(salary_user[0])
    salary_user[1] = int(salary_user[1])
    update_salary(id_user, salary_user)
    time_keyboard = [['15 min', '30 min'],
                     ['1 hour', '2 hours']]
    markup = ReplyKeyboardMarkup(time_keyboard, one_time_keyboard=True)
    update.message.reply_text("Введите частоту, с которой должен производиться опрос сайта: ", reply_markup=markup)
    return 4


def final_set(update, context):
    global salary_user, specialization_user, iter_time
    iter_time = update.message.text
    t = iter_time.split()[1]
    if t[0] == 'm':
        iter_time = int(iter_time.split()[0])
    else:
        iter_time = int(iter_time.split()[0] * 60)

    update.message.reply_text(
        "Отлично! Теперь вы не пропустите ни одну вакансию на профессию {} с зарплатой {} - {}руб".format(
            specialization_user, salary_user[0], salary_user[1]))

    while running:
        get_vacancies(update, context)
        time.sleep(iter_time * 60)


#@repeat(every(iter_time).seconds)
def get_vacancies(update, context):
    global page
    jobs = getJobs(id_user, specialization_user, salary_user, page)
    if jobs:
        update.message.reply_text("Не пропустите новые вакансии!")
        for job in jobs:
            update.message.reply_text("Должность: {}\n"
                                      "Город: {}\n"
                                      "Зарплата: {}\n"
                                      "Опубликовано: {}\n"
                                      "Подробнее: {}".format(job["name"], job["city"], job["salary"],
                                                             job["published_at"],
                                                             job["url"]))
    else:
        update.message.reply_text(
            "К сожалению, вакансий по такому фильтру пока что нет, но возможно, появятся в будующем")
    page = 0


def more(update, context):
    global page
    page += 1
    get_vacancies(update, context)


def stop(update, context):
    update.message.reply_text("Ok")
    global running
    running = False


def resume(update, context):
    update.message.reply_text("Ok")
    running = True


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


def get_my_data(update, context):
    specialization = get_specialization(id)
    salary = get_salary(id)
    update.message.reply_text(f"Ваша должность: {specialization}\nваш диапазон зарплаты {salary[0]} - {salary[1]}")


def main():
    updater = Updater('1748088290:AAECIUFFgjPBCLhZEITijjas3Gf-l1U_F-I', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, set_specialization, pass_user_data=True)],
            2: [MessageHandler(Filters.text, reception_specialization)],
            3: [MessageHandler(Filters.text, set_update_time)],
            4: [MessageHandler(Filters.text, final_set, pass_user_data=True)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(CommandHandler("set_specialization", set_specialization))
    dp.add_handler(CommandHandler("set_salary", reception_specialization))
    dp.add_handler(CommandHandler("set_update_time", set_update_time))
    dp.add_handler(CommandHandler("open", open_keyboard))
    dp.add_handler(CommandHandler("more", more))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("resume", resume))
    dp.add_handler(CommandHandler("get_my_data", get_my_data))
    
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()