"""
Модуль предназначен для постоянного изменения имен классов в html и css коде.
С целью усложнить или сделать невозможным их парсинг.
"""
import random
import re
import string
from typing import Union
from bs4 import BeautifulSoup as BSoup
import cssutils


class CodeEncrypt:
    """
    Класс реализует получение имен классов в html и css коде,
    динамически изменяет их.
    """

    def __init__(
            self,
            css_code: Union[list, str] = '',
            html_code: str = ''
    ) -> None:
        if isinstance(css_code, list):
            css_code = '\n'.join(css_code)
        if html_code.find('<style>') == -1:
            self.code = f'<html><body><style>{css_code}</style></body></html>'
        else:
            code_list = html_code.split('<style>')
            code_list.insert(1, css_code)
            self.code = '<style>'.join(code_list)
        self.soup = BSoup(self.code, 'html.parser')
        self.code = str(self.soup)
        self.css_classes = self._get_css_classes()
        self.html_classes = self._get_html_classes()
        self.new_css = self._rename_css_classes(self.css_classes)

    def encrypt(self) -> tuple:
        """
        Запускает код.
        Returns:
            tuple[0]: html код с измененными классами.
            tuple[1]: css код с измененными классами.
        """
        self._encrypt_html()
        self._encrypt_css()
        self.code = self._clean_html()
        return self.code, self.css_classes

    def _encrypt_html(self) -> None:
        """
        Заменяет оригинальные названия html классов на сгенерированные.
        """
        for html_class in self.html_classes:
            html = str(html_class)
            for k, class_ in enumerate(html_class['class']):
                html_class['class'][k] = self.new_css.get(
                    f'.{class_}',
                    self.__create_name_new_class()
                )
            self.code = self.code.replace(html, str(html_class))

    def _encrypt_css(self) -> None:
        """
        Заменяет оригинальные названия css классов на сгенерированные.
        """
        for old_css, new_css in self.new_css.items():
            if old_css in self.css_classes:
                self.css_classes[new_css] = self.css_classes.pop(old_css)

    def _clean_html(self) -> str:
        """
        Удаляет из кода html все вхождения с тэгом style.

        Returns:
            str: очищенный html.
        """
        pattern = r'<[ ]*style.*?\/[ ]*style[ ]*>'
        text = re.sub(pattern, '', self.code, flags=(
                re.IGNORECASE | re.MULTILINE | re.DOTALL
        ))
        return text

    def _rename_css_classes(self, css_classes: dict) -> dict:
        """
        Создает словарь с новыми именами для классов css в виде значений.

        Args:
            css_classes: оригинальные классы css стилей.
        Returns:
            dict: словарь, ключами которого являются старые названия
            классов, а значения случайно сгенерированные названия классов.
        """
        new_css = {}
        for i in css_classes.keys():
            if i[0] == '.':
                new_css[i] = self.__create_name_new_class()
        return new_css

    def _get_html_classes(self) -> list:
        """
        Получает все классы из html кода.

        Returns:
            dict: словарь с классами.
        """
        classes = []
        for element in self.soup.find_all(class_=True):
            classes.append(element)
        return classes

    def _get_css_classes(self) -> dict:
        """
        Получает все классы из css кода.

        Returns:
            dict: словарь с css стилями.
        """
        selectors = {}
        for styles in self.soup.select('style'):
            css = cssutils.parseString(styles.encode_contents())
            for rule in css:
                if rule.type == rule.STYLE_RULE:
                    style = rule.selectorText
                    selectors[style] = {}
                    for item in rule.style:
                        propertyname = item.name
                        value = item.value
                        selectors[style][propertyname] = value
        return selectors

    def __create_name_new_class(self) -> str:
        """
        Создает новое имя для класса.

        Returns:
            Рандомно сгенерированная строка из 16 литер.
        """
        letters = string.ascii_letters
        return ''.join([random.choice(letters) for _ in range(16)])
