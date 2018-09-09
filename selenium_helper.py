from selenium import webdriver
import time
import status

def open(url):
    driver = webdriver.Chrome()
    while True:
        if driver.current_url in ["data:,", "https://reserve.tokyodisneyresort.jp/fo/restaurant/index.html"]:
            driver.get(url)
            time.sleep(0.1)
            continue
        time.sleep(0.2)
        print("o",end="")
        status.Restaurant.parse(driver.page_source)

        time.sleep(20)
        if driver.current_url==url:
            driver.get(url)
            print("o", end="",flush=True)


if __name__ == '__main__':
    open(
        url="https://reserve.tokyodisneyresort.jp/restaurant/search/?useDate={date}&adultNum=2&childNum=0&childAgeInform=&restaurantType=5&nameCd=&wheelchairCount=0&stretcherCount=0&keyword=&reservationStatus=0".format(
            date='20180930'
        )
    )
