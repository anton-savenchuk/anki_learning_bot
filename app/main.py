from bs4 import BeautifulSoup
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


def get_cambridge_data(keyword):
    url = f"https://dictionary.cambridge.org/us/dictionary/english/{keyword}"
    html = requests.get(url, headers=headers, timeout=6)

    soup = BeautifulSoup(html.text, features="html.parser")

    return soup


def get_online_translator_data(keyword):
    url = f"https://www.online-translator.com/translation/english-russian/{keyword}"
    html = requests.get(url, headers=headers, timeout=6)

    soup = BeautifulSoup(html.text, features="html.parser")

    return soup


if __name__ == "__main__":
    # print(get_cambridge_data(input().lower()))
    # print(get_online_translator_data(input().lower()))
