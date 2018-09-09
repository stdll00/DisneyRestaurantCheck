import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import os
import time
import urllib.request

URL = "https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate={date}&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0".format(
    date='20180930'
)


class Restaurant:
    def __init__(self):
        pass

    def _fetch(self):
        session = requests.session()
        r = session.get(URL,timeout=5)
        return r.text
        #with urllib.request.urlopen(URL) as res:
        #    body = res.read()
        #    return body
    @classmethod
    def parse(cls, text):
        soup = BeautifulSoup(text, "lxml")
        # self.parse_from_id(soup.find("ul",id = "ul_XXXRLSSDZA004"))
        for i in range(7):
            # check
            restaurant_id = "#restaurant_{}".format(i)
            if not soup.select(restaurant_id):
                if (i == 0): print("f", end="",flush=True)
                break
            restaurant_name = soup.select(restaurant_id + " > div.header > h2 ")[0].text.strip()
            reserve_ids = [tag['id'] for tag in soup.select(restaurant_id)[0].find_all('ul', class_='cf') if
                           tag.get('id')
                           ]

            for reserve_id in reserve_ids:
                cls.parse_from_id(soup, reserve_id, restaurant_name)

    @staticmethod
    def parse_from_id(soup, tag_id, restaurant_name):
        tag = soup.find("ul", id=tag_id)
        assert isinstance(tag, Tag)
        for child_tag in tag.find_all("li"):
            if child_tag.get('class')[0] == 'blank':
                continue
            r_time = child_tag.find('p', class_='time').text.strip()
            state = child_tag.find('p', class_='text').text.strip()
            if state == "満席" or state == "受付終了":
                continue
            message = restaurant_name + " " + r_time + " " + state
            print(message)
            os.system("osascript -e 'display notification \"{}\"'".format(message))

    def run(self):
        text = self._fetch()
        self.parse(text)


if __name__ == '__main__':
    print(URL)
    while True:
        print("s", end="",flush=True)
        try:
            Restaurant().run()
        except (requests.exceptions.ReadTimeout,requests.exceptions.ConnectTimeout):
            print("t",end="",flush=True)
        except:
            print("Error")
            import traceback

            traceback.print_exc()
            time.sleep(1)
        time.sleep(1)