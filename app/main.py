from bs4 import BeautifulSoup
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


def get_cambridge_data(keyword):
    keyword = keyword.lower()
    url = f"https://dictionary.cambridge.org/us/dictionary/english/{keyword}"
    html = requests.get(url, headers=headers, timeout=6)

    soup = BeautifulSoup(html.text, features="html.parser")

    raw_sound = soup.find(attrs={"type": "audio/mpeg"})
    url_sound = "https://dictionary.cambridge.org" + raw_sound.get("src")

    response = requests.get(url_sound, headers=headers, timeout=6)
    with open(f"sounds/{keyword}.mp3", "wb") as sound:
        sound.write(response.content)


def get_online_translator_data(keyword):
    url = f"https://www.online-translator.com/translation/english-russian/{keyword}"
    html = requests.get(url, headers=headers, timeout=6)

    soup = BeautifulSoup(html.text, features="html.parser")

    return soup


if __name__ == "__main__":
    get_cambridge_data(input().lower())
    # print(get_online_translator_data(input().lower()))
