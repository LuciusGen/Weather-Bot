from WheatherLoaders.Loaders.UrlLoader import UrlLoader
from bs4 import BeautifulSoup


class RP5Loader(UrlLoader):
    """На сайте rp5 краткая информация о погоде содержится в метаинформации по индексу 1"""
    def __init__(self, city_name: str):
        self.site_name = "rp5"
        super().__init__(city_name)

    def _parse(self, soup: BeautifulSoup):
        tmp_meta_weather = soup.find_all("meta")[1].attrs['content']
        today_weather = tmp_meta_weather.split("Завтра")[0]

        return today_weather


if __name__ == '__main__':
    rp5_loader = RP5Loader("Белебей")
    print(rp5_loader.try_to_parse_weather())
