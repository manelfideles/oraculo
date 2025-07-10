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
    # The original string (d.get_text(strip=True) will always 
    # contain two occurrences of bracket-enclosed content (e.g. '[Brasil][Brasil] ...').
    # This removes the first occurrence of bracket-enclosed content
    definitions = [
        re.sub(r'\[.*?\]', '', d.get_text(strip=True), 1) 
        for d in div.select('div[class*="dp-definicao-linha"]')
    ]

    keys = ["word", "syllables", "pronounciation", "word_class"]
    values = []
    for elem, classname in [
        ("span", "varpt"),
        ("span", "titpalavra"),
        ("span", "dp-ortoepia ortoepia dp-so"),
        ("strong", "varpt ml-12 pt-12 pb-4 --pequeno"),
    ]:
        try:
            field_contents = div.find(elem, class_=classname).contents
            field = field_contents[int(len(field_contents) > 1)]
            text = re.sub(r"\s+", " ", field.text).strip()
        except AttributeError:
            text = ""
        values.append(text)

    message_parts = dict(zip(keys, values))
    message_parts["definitions"] = list(set(definitions))

    return message_parts


def format_message(message_parts) -> str:
    return f"""
[{datetime.now().isoformat()[:10]}]

*{message_parts["word"]}*
{message_parts["pronounciation"] or message_parts["syllables"]}

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
    send_to_slack(word)
