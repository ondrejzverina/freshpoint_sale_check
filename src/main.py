"""Script for checking sales in Digiteq Automotive freshpoints"""
import json
import time
import requests
from bs4 import BeautifulSoup
import simpleaudio as sa

with open("../config/config.json", encoding="utf-8") as file:
    CONFIG = json.load(file)

URL = {
    "loft": "https://my.freshpoint.cz/device/product-list/48",
    "reception": "https://my.freshpoint.cz/device/product-list/31"
}


def play_alert():
    """Just play audio using simpleaudio module"""
    wave_obj = sa.WaveObject.from_wave_file(CONFIG["alert"])
    play_obj = wave_obj.play()
    play_obj.wait_done()


def check_freshpoint():
    """Check freshpoint for possible sales"""
    sale_list = {
        "loft": {},
        "reception": {}
        }
    while True:
        for place in sale_list.items():
            res = requests.get(URL[place])
            soup = BeautifulSoup(res.content, "html.parser")
            all_items = soup.find_all("div", {"class": "col-6 col-lg-4 mb-3"})
            change_flag = False
            sale_flag = False
            for item in all_items:
                sale = item.find("span",
                    {"style": "position: absolute; top: 25%; left: 13%; font-weight: 900"}
                )
                name = item.find("div", {"class": "col-12 mb-2"}).text.strip()
                price_sale = item.find("span",
                    {"class": "row justify-content-end " \
                        "justify-content-md-center price font-weight-bold"}
                )
                price_normal = item.find("span",
                    {"class": "px-2 font-italic font-weight-bold price"}
                )
                if sale is not None and \
                    (name not in sale_list[place] or \
                        sale_list[place][name] > price_sale.text.strip()):
                    change_flag = True
                    sale_flag = True
                    print(
                        f"Item \"{name}\" in {place} is in sale " \
                            "{sale.text.strip()} for price {price_sale.text.strip()}"
                    )
                    sale_list[place][name] = price_sale.text.strip()
                elif name in sale_list[place] and \
                    price_normal is not None and sale_list[place][name] < price_normal:
                    change_flag = True
                    sale_list[place][name] = price_normal.text.strip()
                    print(f"Item {name} in {place} is already at normal price. You dumb!")
        if not change_flag:
            print("No change :(")
        if sale_flag:
            play_alert()
        time.sleep(120)


def main():
    """Main function for frespoint check"""
    check_freshpoint()


if __name__ == "__main__":
    main()
