import datetime
import os
import threading
import time

import pytz
import telebot
from schedule import every, repeat, run_pending
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from WheatherLoaders.Loaders import GetMeteoinfoData, GetRP5Data, GetForecaData
from database.database_requests import DatabaseRequests

telepot.api.set_proxy('http://proxy.server:3128')

bot = telebot.TeleBot(os.getenv("token"))
main_dev_id = os.getenv("DEV_ID")
donate_url = os.getenv("DONATE")

main_markup = telebot.types.ReplyKeyboardMarkup()
main_markup.row('Получить погоду', 'Настройки')
main_markup.row('Обратная связь', 'Поддержка проекта')
weather_loaders = {
    "rp5": GetRP5Data.RP5Loader(),
    "meteoinfo": GetMeteoinfoData.MeteoinfoLoader(),
    "foreca": GetForecaData.ForecaLoader()
}

os.chdir("database")
db_loader = DatabaseRequests()


def setup_settings():
    pass


@bot.message_handler(commands=["start"])
def print_start_info(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id,
                     "\n".join((r"Привет! Я мастер погоды.",
                                "Я позволяю получить информацию о погоде из различных источников. \n"
                                "Источники погоды: " + ", ".join(weather_loaders.keys()))),
                     reply_markup=main_markup,
                     parse_mode='markdown')
    sent = bot.send_message(message.chat.id, "Пожалуйста введите свой город")
    bot.register_next_step_handler(sent, setup_city)


@bot.message_handler(commands=["help"])
def print_start_info(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id,
                     "\n".join((r"Я мастер погоды.",
                                "Я позволяю получить информацию о погоде из различных источников. \n"
                                "Источники погоды: " + ", ".join(weather_loaders.keys())))
                     )


def setup_city(message):
    user_id = str(message.chat.id)
    city = message.text
    db_loader.insert_city(user_id, city)
    sent = bot.send_message(message.chat.id,
                            "Пожалуйста введите час(по Москве), в которое вам удобно получать актуальную погоду")
    bot.register_next_step_handler(sent, setup_time)


def setup_time(message):
    user_id = str(message.chat.id)
    time = message.text
    try:
        time = int(time)
    except Exception:
        bot.send_message(message.chat.id,
                         "Вы неправильно ввели время. Время будет назначено на 12 часов")
        time = "12"

    db_loader.insert_time(user_id, time)
    db_loader.insert_sites(message.chat.id)

    bot.send_message(message.chat.id,
                     "Спасибо, настройка успешно завершена. \n"
                     "Получившееся информация: \n"
                     "Время: {} \n"
                     "Город: {}"
                     .format(db_loader.select_time(user_id=user_id)[1].hour, db_loader.select_city(user_id=user_id)[1])
                     )


@bot.message_handler(content_types=['text'])
def send_text(message):
    """Buttons settings"""
    if message.text == 'Получить погоду':
        user_id = str(message.chat.id)
        weather_res = get_weather(user_id)
        if weather_res is not None:
            if len(weather_res) > 0:
                bot.send_message(message.chat.id, "\n".join(weather_res))
            else:
                bot.send_message(message.chat.id,
                                 "У нас не получилось найти информацию ни в одном из ресурсов,"
                                 "попробуйте изменить настройки")
        else:
            bot.send_message(message.chat.id,
                             "Мы не нашли информацию о вас в базе данных, пожалуйста введите команду /start"
                             " и введите информацию")

    if message.text == 'Настройки':
        user_id = str(message.chat.id)
        user_city = db_loader.select_city(user_id)[1]
        user_time = db_loader.select_time(user_id)[1].hour

        bot.send_message(message.chat.id,
                         "Ваш текущий город {}\n"
                         "Ваше текущее время {}".format(user_city, user_time),
                         reply_markup=update_settings_markup())
        pass

    if message.text == 'Обратная связь':
        sent = bot.send_message(message.chat.id,
                                "Пожалуйста введите сообщение, мы обязательно его обработаем и учтем!")
        bot.register_next_step_handler(sent, setup_form)

    if message.text == 'Поддержка проекта':
        bot.send_message(message.chat.id,
                         "Для поддержки нашего проекта используйте следующую ссылку. "
                         "Ваша поддержка позволит нам работать более активно.")
        bot.send_message(message.chat.id, donate_url)
        pass


def update_settings_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Город", callback_data="city"),
               InlineKeyboardButton("Время", callback_data="time"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "city":
        sent = bot.send_message(call.message.chat.id, "Введите ваш текущий город")
        bot.register_next_step_handler(sent, update_city)
    elif call.data == "time":
        sent = bot.send_message(call.message.chat.id, "Введите время, удобное для получения погоды")
        bot.register_next_step_handler(sent, update_time)


def update_city(message):
    user_id = str(message.chat.id)
    db_loader.update_city(user_id, message.text)
    user_city = db_loader.select_city(user_id)[1]
    user_time = db_loader.select_time(user_id)[1].hour

    bot.send_message(message.chat.id,
                     "Ваш текущий город {} \n "
                     "Ваше текущее время {}".format(user_city, user_time),
                     reply_markup=update_settings_markup())


def update_time(message):
    user_id = str(message.chat.id)
    time = message.text

    try:
        time = int(time)
        db_loader.update_time(user_id, time)
    except Exception:
        bot.send_message(message.chat.id,
                         "Вы неправильно ввели время. Время не будет изменено")

    user_city = db_loader.select_city(user_id)[1]
    user_time = db_loader.select_time(user_id)[1].hour

    bot.send_message(message.chat.id,
                     "Ваш текущий город {} \n "
                     "Ваше текущее время {}".format(user_city, user_time),
                     reply_markup=update_settings_markup())


def get_weather(user_id: str):
    if db_loader.check_user_in_db(user_id):
        city = db_loader.select_city(user_id)[1]
        sites = db_loader.select_sites(user_id)
        weather_res = []
        for i in sites:
            try:
                weather_info = weather_loaders[i].try_to_parse_weather(city)
                if weather_info:
                    weather_res.append("Инф. с сайта: " + i + "\n" + weather_info)
            except Exception:
                continue
        return weather_res

    return None


def setup_form(message):
    text = message.text
    bot.send_message(main_dev_id, text + "\n User_id = " + str(message.chat.id))


@repeat(every().hour.at(":00"))
def load_weather_by_hour():
    time_zone = pytz.timezone('Europe/Moscow')
    now_hour = datetime.datetime.now().astimezone(tz=time_zone).hour

    get_weather_by_user_time(now_hour)


def get_weather_by_user_time(now_hour: int):
    users_and_time = db_loader.select_all_user_by_time(now_hour)

    if users_and_time is None:
        return

    if type(users_and_time) is not list:  # if one user with such time
        users_and_time = [users_and_time]

    for user, _ in users_and_time:
        weather_res = get_weather(user)
        if len(weather_res) > 0:
            bot.send_message(user, "\n".join(weather_res))


def run_bot():
    bot.polling(none_stop=True)


def run_schedulers():
    while True:
        run_pending()
        time.sleep(1)


if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_schedulers)
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
