from abc import ABC, abstractmethod
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from googlesearch import search


class UrlLoader(ABC):
    """
    Разрешенные сайты: rp5.ru, meteoinfo, world-weather, погода mail.ru
    Запрещенные сайты: гисметео, яндекс, accuweather, foreca, google
    Обработанные сайты: rp5.ru, meteoinfo, погода mail.ru
    TODO посмотреть как можно получить информацию с запрещенных сайтов
    TODO если нужно(проанализировать) добавить обработку рядов сайта на тот случай, если нужный не находится сразу
    """

    def __init__(self):
        self._google_request = ""
        self.site_name = ""

    def _get_site_name(self):
        return self.site_name

    def _get_url_correct(self, url: str):
        if self._get_site_name() in url:
            return True

    def _get_url(self):
        return next(search(self._google_request, tld="co.in", num=1))

    @abstractmethod
    def _parse(self, soup: BeautifulSoup):
        pass

    def try_to_parse_weather(self, city_name: str):
        self._google_request = self.site_name + " " + city_name
        url = self._get_url()
        if not self._get_url_correct(url):
            return None

        try:
            req = Request(url)
            req.add_header('User-Agent', 'PostmanRuntime/7.6.0')
            html_file = urlopen(req)
            soup = BeautifulSoup(html_file, "html.parser")

            return self._parse(soup)
        except Exception:
            return None
