from WheatherLoaders.Loaders.UrlLoader import UrlLoader
from bs4 import BeautifulSoup


class MeteoinfoLoader(UrlLoader):
    """На сайте на некоторых городах приходит информация и по области,
    таким образом может быть ситуация с некорректной обработкой."""
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
               "Ночью: Максимальная температура %s, ожидаемые погодные условия: %s \n" \
               % (max_day_t_today, short_day_info, max_night_t_today, short_night_info)


if __name__ == '__main__':
    meteoinfo_loader = MeteoinfoLoader()
    print(meteoinfo_loader.try_to_parse_weather("Санкт-Петербург"))
