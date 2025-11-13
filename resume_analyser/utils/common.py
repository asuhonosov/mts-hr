import json
from pathlib import Path
from typing import Any

import requests
from bs4 import BeautifulSoup
import streamlit as st
from urllib.parse import urlparse, urlunparse

DataRow = dict[str, Any]

def read_html_text(html_path: str) -> str:
    with open(html_path) as f:
        return BeautifulSoup(f.read()).text


def load_json_lines(file_path: str | Path) -> list[DataRow]:
    with open(file_path) as f:
        return [json.loads(line) for line in f.readlines()]


def save_json_line(file_path: str | Path, data: DataRow, mode: str = 'a'):
    with open(file_path, mode) as fw:
        fw.write(json.dumps(data, ensure_ascii=False))
        fw.write('\n')


def save_all_json_lines(file_path: str | Path, all_data: list[DataRow], mode: str = 'w'):
    with open(file_path, mode) as fw:
        for data in all_data[:-1]:
            fw.write(json.dumps(data, ensure_ascii=False))
            fw.write('\n')

        fw.write(json.dumps(all_data[-1], ensure_ascii=False))


def highlight_text(text, positive_parts, doubt_parts, negative_parts):
    html_text = text.replace('\n', '<br>')

    for part in positive_parts:
        if part in text:
            html_text = html_text.replace(
                part,
                f'<span style="background-color: rgba(0, 255, 0, 0.3); padding: 2px; border-radius: 3px;">{part}</span>'
            )

    for part in doubt_parts:
        if part in text:
            html_text = html_text.replace(
                part,
                f'<span style="background-color: rgba(255, 255, 0, 0.3); padding: 2px; border-radius: 3px;">{part}</span>'
            )

    for part in negative_parts:
        if part in text:
            html_text = html_text.replace(
                part,
                f'<span style="background-color: rgba(255, 0, 0, 0.3); padding: 2px; border-radius: 3px;">{part}</span>'
            )

    return html_text


def get_text_from_url(url: str, need_normalize: bool = False) -> str | None:
    html = scrap_html(url=url)
    if html is None:
        return None

    return extract_text_from_html(html=html, need_normalize=need_normalize)


def scrap_html(url: str) -> str | None:
    try:
        # cookies_line = '__ddg10_=1752210496; __ddg1_=BKO8Xas6ZHhOf0dILd9B; __ddg8_=bB70hiWN6ZGg5IdC; __ddg9_=93.158.188.122; _xsrf=7b0b14be8b52daf3483858a4b5ea6b36; crypted_hhuid=6A015BAD93FD6B3662710097A0483E455DA6CCE392AD12B4455AA6E68F0893D2; display=desktop; hhrole=anonymous; hhtoken=g!m0QpSEhrkmYlMq_cN2L1VPKf!M; hhuid=qG0XxQh356MDIWhwm!wo2Q--; region_clarified=NOT_SET; regions=1'
        # cookies = dict(part.strip().split('=') for part in cookies_line.split(';'))
        # print(f'{cookies=}')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    except Exception as e:
        st.error(f"Ошибка при загрузке URL: {e}")
        return None


def extract_text_from_html(html: str, need_normalize: bool = False) -> str:
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Удаляем скрипты и стили
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        # Очищаем текст от лишних пробелов и переносов строк
        if need_normalize:
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        st.error(f"Ошибка при парсинге html: {e}")
        return None


def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    # Удаляем скрипты и стили
    for script in soup(["script", "style"]):
        script.extract()

    return str(soup)


def clean_url(url):
    """
    Очищает URL от параметров после знака вопроса.
    Сохраняет протокол, домен и путь.

    Args:
        url (str): Исходный URL

    Returns:
        str: Очищенный URL без параметров запроса
    """
    if not url:
        return url

    # Разбираем URL на компоненты
    parsed_url = urlparse(url)

    # Собираем URL обратно, но без параметров запроса и фрагмента
    clean_parsed = parsed_url._replace(params='', query='', fragment='')

    # Преобразуем компоненты обратно в строку URL
    return urlunparse(clean_parsed).strip()