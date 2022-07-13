from bs4 import BeautifulSoup

from WheatherLoaders.Loaders.UrlLoader import UrlLoader


class ForecaLoader(UrlLoader):
    """Foreca weather information loader"""

    def __init__(self):
        super().__init__()
        self.site_name = "foreca погода"

    def _get_site_name(self):
        return "foreca"

    def _parse(self, soup: BeautifulSoup):
        today_weather = soup.find_all(class_="c2_a")[0].contents[1]
        max_day_t = today_weather.contents[7].contents[1].contents[0]
        short_info = today_weather.contents[4].attrs["title"]
        night_t = today_weather.contents[10].contents[1].contents[0]

        return "Максимальная температура днём: %s, ночью: %s, ожидаемые погодные условия: %s" % \
               (max_day_t, night_t, short_info)
