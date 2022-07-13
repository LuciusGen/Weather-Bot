from bs4 import BeautifulSoup

from WheatherLoaders.Loaders.UrlLoader import UrlLoader


class RP5Loader(UrlLoader):
    """RP5 weather information loader"""

    def __init__(self):
        super().__init__()
        self.site_name = "rp5"

    def _parse(self, soup: BeautifulSoup):
        tmp_meta_weather = soup.find_all("meta")[1].attrs['content']
        today_weather = tmp_meta_weather.split("Завтра")[0]

        return today_weather
