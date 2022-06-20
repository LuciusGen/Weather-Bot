from WheatherLoaders.Loaders.UrlLoader import UrlLoader
from bs4 import BeautifulSoup
from googlesearch import search


class YandexLoader(UrlLoader):
    """На сайте rp5 краткая информация о погоде содержится в метаинформации по индексу 1"""
    def __init__(self):
        super().__init__()
        self.site_name = "яндекс погода"

    def _get_site_name(self):
        return "yandex"

    def _get_url(self):
        search_res = search(self._google_request, tld="co.in", num=10, stop=10)
        for i in search_res:
            if "yandex.ru/pogoda" in i:
                return i
        else:
            return None

    def _parse(self, soup: BeautifulSoup):
        weather_info = soup.find_all(class_="forecast-briefly__day forecast-briefly__day_sunday forecast-briefly__day_weekend swiper-slide")
        today_info = weather_info[0].contents[0].contents[0].contents

        day_info = today_info[3].contents[1].contents[0]
        night_info = today_info[4].contents[1].contents[0]
        short_info = today_info[5].contents[0]

        return "Температура днём : %s, ночью : %s, ожидаемые погодные условия : %s" % (day_info, night_info, short_info)
