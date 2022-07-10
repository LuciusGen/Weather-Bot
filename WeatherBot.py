import os
import threading

from schedule import every, repeat, run_pending
import time
import pytz
import telebot
from WheatherLoaders.Loaders import GetMailData, GetMeteoinfoData, GetRP5Data, GetForecaData, \
    GetGismeteoData, GetYandexData, GetAccuweatherData
from database.database_requests import DatabaseRequests
import datetime

bot = telebot.TeleBot(os.getenv("token"))
main_dev_id = 370493821

main_markup = telebot.types.ReplyKeyboardMarkup()
main_markup.row('Получить погоду', 'Изменить настройки')
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


def setup_city(message):
    user_id = str(message.chat.id)
    city = message.text
    db_loader.insert_city(user_id, city)
    sent = bot.send_message(message.chat.id,
                            "Пожалуйста введите время(по Москве), в которое вам удобно получать актуальную погоду")
    bot.register_next_step_handler(sent, setup_time)


def setup_time(message):
    user_id = str(message.chat.id)
    time = message.text
    db_loader.insert_time(user_id, time)
    db_loader.insert_sites(message.chat.id)

    bot.send_message(message.chat.id,
                     "Спасибо, настройка успешно завершена. \n"
                     "Получившееся информация: \n"
                     "Время: " + db_loader.select_time(user_id=user_id).hour + "\n"
                     "Город: " + db_loader.select_city(user_id=user_id) + "\n")


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

    if message.text == 'Изменить настройки':
        # TODO получить текущие настройки и сделать удобный инфтерфейс для их изменения
        pass

    if message.text == 'Обратная связь':
        sent = bot.send_message(message.chat.id,
                                "Пожалуйста введите сообщение, мы обязательно его обработаем и учтем!")
        bot.register_next_step_handler(sent, setup_form)

    if message.text == 'Поддержка проекта':
        # TODO добавить ссылку на донат проекту
        pass


def get_weather(user_id: str):
    if db_loader.check_user_in_db(user_id):
        city = db_loader.select_city(user_id)[1]
        sites = db_loader.select_sites(user_id)
        weather_res = []
        for i in sites:
            weather_info = weather_loaders[i].try_to_parse_weather(city)
            if weather_info:
                weather_res.append("Инф. с сайта: " + i + "\n" + weather_info)

        return weather_res

    return None


def setup_form(message):
    text = message.text
    bot.send_message(main_dev_id, text + "\n User_id = " + str(message.chat.id))


@repeat(every(1).minutes)
def load_weather_by_hour():
    time_zone = pytz.timezone('Europe/Moscow')
    now_hour = datetime.datetime.now().astimezone(tz=time_zone).minute % 10

    get_weather_by_user_time(now_hour)


def get_weather_by_user_time(now_hour: int):
    users_and_time = db_loader.select_all_user_by_time(now_hour)

    if users_and_time is None:
        return

    if type(users_and_time) is not list: # if one user with such time
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
