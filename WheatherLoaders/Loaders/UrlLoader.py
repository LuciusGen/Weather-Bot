from googlesearch import search
from urllib import request
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class UrlLoader(ABC):
    """
    Разрешенные сайты: rp5.ru, meteoinfo, world-weather, погода mail.ru
    Запрещенные сайты: гисметео, яндекс, accuweather, foreca, google
    Обработанные сайты: rp5.ru, meteoinfo, погода mail.ru
    TODO посмотреть как можно получить информацию с запрещенных сайтов
    TODO если нужно(проанализировать) добавить обработку рядов сайта на тот случай, если нужный не находится сразу
    """
    def __init__(self, city_name: str):
        self._google_request = self._get_site_name() + " " + city_name
        self.site_name = ""

    def _get_site_name(self):
        return self.site_name

    def _get_url_correct(self, url: str):
        if self.site_name in url:
            return True

    def _get_url(self):
        return next(search(self._google_request, tld="co.in", num=1))

    @abstractmethod
    def _parse(self, soup: BeautifulSoup):
        pass

    def try_to_parse_weather(self):
        url = self._get_url()
        if not self._get_url_correct(url):
            return None

        try:
            html_file = request.urlopen(url)
            soup = BeautifulSoup(html_file, "html.parser")

            return self._parse(soup)
        except:
            return None
