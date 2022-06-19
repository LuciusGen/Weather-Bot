from WheatherLoaders.Loaders.UrlLoader import UrlLoader
from bs4 import BeautifulSoup


class AccuweatherLoader(UrlLoader):
    """На сайте rp5 краткая информация о погоде содержится в метаинформации по индексу 1"""
    def __init__(self):
        super().__init__()
        self.site_name = "accuweather погода"

    def _get_site_name(self):
        return "accuweather"

    def _parse(self, soup: BeautifulSoup):
        full_info = soup.find_all(class_="card-content")

        day_info = full_info[0]
        night_info = full_info[1]

        day_t = day_info.contents[1].contents[3].contents[1].contents[0]
        day_short = day_info.contents[3].contents[0]

        night_t = night_info.contents[1].contents[3].contents[1].contents[0]
        night_short = night_info.contents[3].contents[0]

        return "Температура днём : %s, вечером : %s, ожидаемые погодные условия днём: %s, вечером: %s" % \
               (day_t, night_t, day_short, night_short)
