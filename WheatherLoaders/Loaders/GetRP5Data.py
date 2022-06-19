from WheatherLoaders.Loaders.UrlLoader import UrlLoader
from bs4 import BeautifulSoup


class RP5Loader(UrlLoader):
    """На сайте rp5 краткая информация о погоде содержится в метаинформации по индексу 1"""
    def __init__(self):
        super().__init__()
        self.site_name = "rp5"

    def _parse(self, soup: BeautifulSoup):
        tmp_meta_weather = soup.find_all("meta")[1].attrs['content']
        today_weather = tmp_meta_weather.split("Завтра")[0]

        return today_weather
