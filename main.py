import requests
from bs4 import BeautifulSoup
import json


def get_data():
    for i in range (1, 15):
        url_list = []
        url = f"https://pizzmaster.ru/shop/all/{i}"
        headers = {
            "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; v = b3; q = 0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        req = requests.get(url, headers=headers)
        src = req.text
        # print(src)

        with open("index.html", "w", encoding="utf-8") as file:
            file.write(src)

        with open("index.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        position = soup.find_all("a", class_="absolute")
        for a in position:
            url_list.append("https://pizzmaster.ru" + a["href"])
        position_list_result = []
        for url_1 in url_list:
            # print(count)
            # print(url)

            req_1 = requests.get(url=url_1, headers=headers)
            try:

                soup_1 = BeautifulSoup(req_1.text, "lxml")
                position_info_block = soup_1.find("div", class_="product-info-block")
                position_name = position_info_block.find("h1").text.strip()
                position_description = position_info_block.find("div", class_="introtext").text.strip()
                position_price = position_info_block.find("div", class_="price-wrap").find("span").text.strip()
                position_picture = "https://pizzmaster.ru" + soup_1.find("div", class_="product-carousel").find("a").get("href")

                position_list_result.append(
                    {
                        "Position name": position_name,
                        "Position description": position_description,
                        "Position price": position_price,
                        "Position picture": position_picture

                    }
                )

            except Exception as ex:
                print(ex)
                print("Мда...Походу ошибка...")

        with open("position_list_result.json", "a", encoding="utf-8") as file:
            json.dump(position_list_result, file, indent=4, ensure_ascii=False)
        print(position_list_result)

def main():
    get_data()

if __name__ == "__main__":
    main()
