import os
import telebot
from WheatherLoaders.Loaders import GetMailData, GetMeteoinfoData, GetRP5Data

bot = telebot.TeleBot(os.environ["token"])
main_markup = telebot.types.ReplyKeyboardMarkup()
main_markup.row('Получить погоду', 'Изменить настройки')
main_markup.row('Обратная связь', 'Поддержка проекта')
weather_loaders = {
    "rp5": GetRP5Data.RP5Loader(),
    "mail": GetMailData.MailLoader(),
    "meteoinfo": GetMeteoinfoData.MeteoinfoLoader()
}


def setup_settings():
    pass


@bot.message_handler(commands=["start"])
def print_start_info(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id,
                     "\n".join((r"Привет\! Я мастер погоды\!",
                                "Я позволяю получить информацию о погоде из различных источников")),
                     reply_markup=main_markup,
                     parse_mode='markdown')
    setup_settings()


@bot.message_handler(content_types=['text'])
def send_text(message):
    """Buttons settings"""
    if message.text == 'Получить погоду':
        weather = []
        for (key, value) in weather_loaders.items():
            weather.append("Информация с сайта %s: \n" % key + value.try_to_parse_weather("Санкт-Петербург"))
        bot.send_message(message.chat.id, "\n\n".join(weather))

    if message.text == 'Изменить настройки':
        pass

    if message.text == 'Обратная связь':
        pass

    if message.text == 'Поддержка проекта':
        pass


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            pass
