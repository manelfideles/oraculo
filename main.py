import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, NavigableString, Tag


def get_page(url: str) -> requests.Response:
    return requests.get(url)


def extract_daily_word_div(page: requests.Response) -> Tag | NavigableString:
    html = page.text
    soup = BeautifulSoup(html, "html.parser")
    element = soup.find("div", class_="dp-definicao")
    return element


def get_message_parts(div: Tag | NavigableString) -> dict:
    definitions = [
        re.sub(r"\s+", " ", s.text).strip()
        for s in div.find_all("p", class_="py-4 dp-definicao-linha")
    ]

    return {
        "word": div.find("span", class_="varpt").text,
        "syllables": div.find("span", class_="titpalavra").text,
        "word_class": div.find("h4", class_="varpt ml-12 pt-12 pb-4 --pequeno").text,
        "definitions": definitions,
    }


def format_message(message_parts) -> str:
    return f"""
[{datetime.now().isoformat()[:10]}]

**{message_parts["word"]}**
{message_parts["syllables"]}

_{message_parts["word_class"]}_
{'\n'.join(message_parts['definitions'])}
"""


def send_to_slack(msg: str) -> requests.Response:
    print(msg)


if __name__ == "__main__":
    page = get_page("https://dicionario.priberam.org/")
    div = extract_daily_word_div(page)
    msg_parts = get_message_parts(div)
    word = format_message(msg_parts)
    send_to_slack(word)
