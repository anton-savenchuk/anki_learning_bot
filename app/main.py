import re

from bs4 import BeautifulSoup
import requests

from _messages import messages


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


def check_keyword(keyword: str) -> tuple[bool, str]:
    """Check keyword for errors."""
    keyword = keyword.lower()
    flag = True
    if " " in keyword:
        flag = False
        fail_message = messages.get("only_one_word")
    elif re.search(r"[^a-zA-Zа]", keyword):
        flag = False
        fail_message = messages.get("only_english_letters")
    elif len(keyword) == 1:
        flag = False
        fail_message = messages.get("length_word")
    else:
        online_translator_data = get_soupe(
            "https://www.online-translator.com/translation/english-russian/",
            keyword,
        )

        flag = len(get_translation(online_translator_data)) >= 1
        fail_message = (
            messages.get("no_mistakes") if flag else messages.get("no_such_word")
        )

    return flag, fail_message


def get_soupe(url: str, keyword: str = "") -> BeautifulSoup:
    """Get BeautifulSoup constructor."""
    url = f"{url}{keyword}"
    html = requests.get(url, headers=headers, timeout=6)

    return BeautifulSoup(html.text, features="html.parser")


def get_translation(soup: BeautifulSoup) -> list:
    """Get a keyword translation."""
    keyword_translation: list = soup.find_all(
        "span",
        class_="result_only sayWord",
        limit=3,
    )

    return [word.text for word in keyword_translation]


def get_example_list(soup: BeautifulSoup, class_: str) -> list:
    """Get examples list of keyword usage."""
    raw_examples: list = soup.find(
        "div",
        id="topSamplesSelSource",
    ).find_all(
        "span",
        class_=class_,
        limit=3,
    )

    example_list: list = []
    for example in raw_examples:
        example = str(example)[len(f'<span class="{class_}">') : -len("</span>")]
        example_list.append(
            example.replace('<span class="samSource">', "")
            .replace('<span class="sourceSample">', "<b>")
            .replace("</span>", "</b>")
        )

    return example_list


def get_sound(soup: BeautifulSoup, keyword: str) -> tuple:
    """Get a keyword sound and url for anki card."""
    raw_sound = soup.find(attrs={"type": "audio/mpeg"})
    url_sound = "https://dictionary.cambridge.org" + raw_sound.get("src")

    response = requests.get(url_sound, headers=headers, timeout=6)
    with open(f"sounds/{keyword}.mp3", "wb") as sound:
        sound.write(response.content)

    return f"sounds/{keyword}.mp3", url_sound


def get_keyword_data(keyword: str) -> dict:
    """Get data from keyword."""
    keyword = keyword.lower()
    cambridge_data = get_soupe(
        "https://dictionary.cambridge.org/us/dictionary/english/", keyword
    )
    online_translator_data = get_soupe(
        "https://www.online-translator.com/translation/english-russian/", keyword
    )
    translation: list = get_translation(online_translator_data)
    examples: tuple = (
        get_example_list(online_translator_data, "samSource"),
        get_example_list(online_translator_data, "samTranslation"),
    )
    sound, sound_url = get_sound(cambridge_data, keyword)

    return {
        "keyword": keyword,
        "translation": translation,
        "examples": examples,
        "sound": sound,
        "sound_url": sound_url,
    }


def get_card_data(keyword_data: dict) -> dict:
    """Get anki card from keyword data."""
    keyword_for_card = keyword_data.get("keyword").title()
    translation_for_card: list = [
        f'<li class="word">{word}</li>' for word in keyword_data.get("translation")
    ]
    translation_for_card: str = "<ul>" + "".join(translation_for_card) + "</ul>"

    example_for_card = keyword_data.get("examples")[0][0]
    example_translate_for_card = keyword_data.get("examples")[1][0]

    examples_for_card: list = [
        f'<p>{exmpl_eng}<br><span class="ghost">{exmpl_ru}</span></p>'
        for exmpl_eng, exmpl_ru in zip(
            keyword_data.get("examples")[0][1:], keyword_data.get("examples")[1][1:]
        )
    ]

    examples_for_card: str = "".join(examples_for_card)
    sound_url = keyword_data.get("sound_url")

    return {
        "keyword": keyword_for_card,
        "example": example_for_card,
        "example_translate": example_translate_for_card,
        "examples": examples_for_card,
        "translation": translation_for_card,
        "sound": sound_url,
    }


if __name__ == "__main__":
    keyword = input().lower()
    flag, fail_message = check_keyword(keyword)

    if flag:
        keyword_data = get_keyword_data(keyword)
        card_data = get_card_data(keyword_data)

        print(keyword_data, card_data)

    else:
        print(fail_message)
