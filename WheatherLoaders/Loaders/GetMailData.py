from WheatherLoaders.Loaders.UrlLoader import UrlLoader
from bs4 import BeautifulSoup
from googlesearch import search


class MailLoader(UrlLoader):
    """На данном сайте картинка содержит в себе информацию о погоде"""
    def __init__(self):
        super().__init__()
        self.site_name = "mail погода"

    def _parse(self, soup: BeautifulSoup):
        today_nfo = soup.find_all(class_="information__content__temperature")

        current_t = today_nfo[0].contents[2].strip()
        short_info_t = today_nfo[0].contents[1].attrs["title"]

        return "Температура: %s, ожидаемые погодные условия: %s" % (current_t, short_info_t)

    def _get_site_name(self):
        return "pogoda.mail"

    def _get_url(self):
        search_res = search(self._google_request, tld="co.in", num=10, stop=10)
        for i in search_res:
            if "pogoda.mail" in i:
                return i
        else:
            return None


if __name__ == '__main__':
    mail_loader = MailLoader()
    print(mail_loader.try_to_parse_weather("Санкт-Петербург"))
