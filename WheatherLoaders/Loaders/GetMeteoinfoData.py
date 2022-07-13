from bs4 import BeautifulSoup

from WheatherLoaders.Loaders.UrlLoader import UrlLoader


class MeteoinfoLoader(UrlLoader):
    """Meteoifo weather information loader"""

    def __init__(self):
        super().__init__()
        self.site_name = "meteoinfo"

    def _parse(self, soup: BeautifulSoup):
        all_info = soup.find_all(class_="td_short_gr")

        max_day_t_today = all_info[17].contents[0].contents[0]
        short_day_info = all_info[9].contents[0].contents[0].attrs['title']

        max_night_t_today = all_info[66].contents[0].contents[0].contents[0]
        short_night_info = all_info[58].contents[0].contents[0].attrs['title']

        return "Днем: Максимальная температура %s, ожидаемые погодные условия: %s \n" \
               "Ночью: Максимальная температура %s, ожидаемые погодные условия: %s" \
               % (max_day_t_today, short_day_info, max_night_t_today, short_night_info)
