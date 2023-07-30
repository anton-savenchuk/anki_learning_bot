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

    return url_sound


def get_online_translator_data(keyword):
    keyword = keyword.lower()
    url = f"https://www.online-translator.com/translation/english-russian/{keyword}"
    html = requests.get(url, headers=headers, timeout=6)

    soup = BeautifulSoup(html.text, features="html.parser")

    raw_keyword_translation = soup.find_all(
        "span",
        class_="result_only sayWord",
        limit=3,
    )
    keyword_translation = []
    for word in raw_keyword_translation:
        keyword_translation.append(word.text)

    raw_english_examples = soup.find(
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

    raw_russian_examples = soup.find(
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
    sound_url = get_cambridge_data(keyword)

    return {
        "keyword": keyword_for_card,
        "example": example_for_card,
        "example_translate": example_translate_for_card,
        "examples": examples_for_card,
        "translation": translation_for_card,
        "sound": sound_url,
    }


if __name__ == "__main__":
    # get_cambridge_data(input().lower())
    # print(get_online_translator_data(input().lower()))
    for item in get_card_data(input().lower()).values():
        print(item)
