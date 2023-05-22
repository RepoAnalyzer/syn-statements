from bs4 import BeautifulSoup
from markdown import markdown

import re


def markdown_to_text(markdown_string):
    """
    Конвертация markdown-текста to обычный текст
    :param markdown_string: Строка в markdown формате
    :return: Строка обычного текста
    """
    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # Удаление сниппетов
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # Удаление ссылок
    html = re.sub(r'<a href=(.*?)>(.*?)</a>', ' ', html)
    html = re.sub(r'https?://\S+', ' ', html)

    # Удаление изображений
    html = re.sub(r'<img (.*?)/>', ' ', html)

    # Удаление специальных символов
    html = re.sub(r'\s', ' ', html)

    # Удаление нескольких пробелов
    html = re.sub(r'\s\s+', ' ', html)

    # Извлечение текста
    soup = BeautifulSoup(html, 'lxml')
    text = ''.join(soup.findAll(string=True))

    return text
