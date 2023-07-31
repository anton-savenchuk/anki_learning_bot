from bs4 import BeautifulSoup
import requests

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


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


def get_sound(soup: BeautifulSoup, keyword: str) -> tuple:
    """Get a keyword sound and url for anki card."""
    raw_sound = soup.find(attrs={"type": "audio/mpeg"})
    url_sound = "https://dictionary.cambridge.org" + raw_sound.get("src")

    response = requests.get(url_sound, headers=headers, timeout=6)
    with open(f"sounds/{keyword}.mp3", "wb") as sound:
        sound.write(response.content)

    return f"sounds/{keyword}.mp3", url_sound


def get_online_translator_data(keyword):
    keyword = keyword.lower()
    online_translator_data = get_soupe(
        "https://www.online-translator.com/translation/english-russian/", keyword
    )

    raw_keyword_translation = online_translator_data.find_all(
        "span",
        class_="result_only sayWord",
        limit=3,
    )
    keyword_translation = []
    for word in raw_keyword_translation:
        keyword_translation.append(word.text)

    raw_english_examples = online_translator_data.find(
        "div",
        id="topSamplesSelSource",
    ).find_all(
        "span",
        class_="samSource",
        limit=3,
    )

    english_example_list = []
    for example in raw_english_examples:
        example = str(example)[24:-7]
        english_example_list.append(
            example.replace('<span class="samSource">', "")
            .replace('<span class="sourceSample">', "<b>")
            .replace("</span>", "</b>")
        )

    raw_russian_examples = online_translator_data.find(
        "div",
        id="topSamplesSelSource",
    ).find_all(
        "span",
        class_="samTranslation",
        limit=3,
    )

    russian_example_list = []
    for example in raw_russian_examples:
        example = str(example)[29:-7]
        russian_example_list.append(
            example.replace('<span class="samTranslation">', "")
            .replace('<span class="sourceSample">', "<b>")
            .replace("</span>", "</b>")
        )

    return keyword_translation, english_example_list, russian_example_list


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
    sound, sound_url = get_sound(cambridge_data, keyword)

    return {
        "keyword": keyword,
        "translation": translation,
        "sound": sound,
        "sound_url": sound_url,
    }


def get_card_data(keyword):
    keyword_for_card = keyword.title()

    (
        keyword_translation,
        english_example_list,
        russian_example_list,
    ) = get_online_translator_data(keyword)

    translation_for_card = []
    for word in keyword_translation:
        translation_for_card.append(f'<li class="word">{word}</li>')

    translation_for_card = "<ul>" + "".join(translation_for_card) + "</ul>"

    example_for_card = english_example_list[0]
    example_translate_for_card = russian_example_list[0]

    examples_for_card = [
        f'<p>{exmpl_eng}<br><span class="ghost">{exmpl_ru}</span></p>'
        for exmpl_eng, exmpl_ru in zip(
            english_example_list[1:], russian_example_list[1:]
        )
    ]

    examples_for_card = "".join(examples_for_card)
    sound_url = get_sound(keyword)[1]

    return {
        "keyword": keyword_for_card,
        "example": example_for_card,
        "example_translate": example_translate_for_card,
        "examples": examples_for_card,
        "translation": translation_for_card,
        "sound": sound_url,
    }


if __name__ == "__main__":
    print(get_keyword_data(input().lower()))
    # print(get_online_translator_data(input().lower()))
    # for item in get_card_data(input().lower()).values():
    #     print(item)
