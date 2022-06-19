import os
import telebot
from WheatherLoaders.Loaders import GetMailData, GetMeteoinfoData, GetRP5Data, GetForecaData, \
    GetGismeteoData, GetYandexData, GetAccuweatherData
from database.database_requests import DatabaseRequests

bot = telebot.TeleBot(os.environ["token"])
main_dev_id = 370493821

main_markup = telebot.types.ReplyKeyboardMarkup()
main_markup.row('Получить погоду', 'Изменить настройки')
main_markup.row('Обратная связь', 'Поддержка проекта')
weather_loaders = {
    "rp5": GetRP5Data.RP5Loader(),
    "Mail": GetMailData.MailLoader(),
    "Meteoinfo": GetMeteoinfoData.MeteoinfoLoader(),
    "Yandex": GetYandexData.YandexLoader(),
    "Foreca": GetForecaData.ForecaLoader(),
    "Gismeteo": GetGismeteoData.GismeteoLoader(),
    "Accuweather": GetAccuweatherData.AccuweatherLoader()
}

os.chdir("database")
db_loader = DatabaseRequests("database.db")


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
                            "Пожалуйста введите время, в которое вам удобно получать актуальную погоду")
    bot.register_next_step_handler(sent, setup_time)


def setup_time(message):
    user_id = str(message.chat.id)
    time = message.text
    db_loader.insert_time(user_id, time)
    db_loader.insert_sites(message.chat.id)


@bot.message_handler(content_types=['text'])
def send_text(message):
    """Buttons settings"""
    if message.text == 'Получить погоду':
        user_id = str(message.chat.id)
        if not db_loader.check_user_in_db(user_id):
            city = db_loader.select_city(user_id)[1]
            sites = db_loader.select_sites(user_id)
            weather_res = []
            for i in sites:
                weather_info = weather_loaders[i].try_to_parse_weather(city)
                if weather_info:
                    weather_res.append("Инф. с сайта: " + i + "\n" + weather_info)

            if len(weather_res) > 0:
                bot.send_message(message.chat.id, "\n".join(weather_res))
            else:
                bot.send_message(message.chat.id, "У нас не получилось найти информацию ни в одном из ресурсов,"
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


def setup_form(message):
    text = message.text
    bot.send_message(main_dev_id, text + "\n User_id = " + str(message.chat.id))


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
