from bs4 import BeautifulSoup
from googlesearch import search

from WheatherLoaders.Loaders.UrlLoader import UrlLoader


class GismeteoLoader(UrlLoader):
    """На сайте rp5 краткая информация о погоде содержится в метаинформации по индексу 1"""

    def __init__(self):
        super().__init__()
        self.site_name = "gismeteo погода"

    def _get_site_name(self):
        return "gismeteo"

    def _get_url(self):
        search_res = search(self._google_request, tld="co.in", num=10, stop=10)
        for i in search_res:
            if "gismeteo" in i and "10-days" not in i:
                return i
        else:
            return None

    def _parse(self, soup: BeautifulSoup):
        today_info = soup.find_all(class_="weathertab weathertab-block tooltip")
        short_info = today_info[0].attrs["data-text"]
        night_t = \
            today_info[0].contents[0].contents[0].contents[2].contents[0].contents[0].contents[0].contents[0].contents[
                0]
        day_t = \
            today_info[0].contents[0].contents[0].contents[2].contents[0].contents[0].contents[1].contents[0].contents[
                0]

        return "Температура днём : %s, ночью : %s, ожидаемые погодные условия : %s" % (day_t, night_t, short_info)
