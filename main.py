import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from dotenv import load_dotenv

load_dotenv()


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
        for s in div.find_all("p", class_=re.compile(r"dp-definicao-linha"))
    ]

    keys = ["word", "syllables", "pronounciation", "word_class"]
    values = []
    for elem, classname in [
        ("span", "varpt"),
        ("span", "titpalavra"),
        ("span", "dp-ortoepia ortoepia dp-so"),
        ("h4", "varpt ml-12 pt-12 pb-4 --pequeno"),
    ]:
        try:
            field = div.find(elem, class_=classname)
            text = re.sub(r"\s+", " ", field.text).strip()
        except AttributeError:
            text = ""
        values.append(text)

    message_parts = dict(zip(keys, values))
    message_parts["definitions"] = definitions

    return message_parts


def format_message(message_parts) -> str:
    return f"""
[{datetime.now().isoformat()[:10]}]

*{message_parts["word"]}*
{message_parts["syllables"]}
{message_parts["pronounciation"]}

_{message_parts["word_class"]}_
{'\n'.join(message_parts['definitions'])}
"""


def send_to_slack(msg: str) -> requests.Response:
    webhook_url = os.environ.get("SLACK_INCOMING_WEBHOOK_URL")
    try:
        response = requests.post(webhook_url, json={"text": msg})
        if response.status_code == 200:
            print("Word of the day sent, check the #word-of-the-day channel.")
    except Exception as e:
        print(f"Could not send the word to Slack: {e}")


if __name__ == "__main__":
    page = get_page("https://dicionario.priberam.org/")
    div = extract_daily_word_div(page)
    msg_parts = get_message_parts(div)
    word = format_message(msg_parts)
    print(word)
    # send_to_slack(word)
