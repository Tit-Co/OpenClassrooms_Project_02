from dataclasses import dataclass, field
from typing import List
from PySide6.QtCore import QObject, Signal
from pathlib import Path

class Book(QObject):
    titleChanged = Signal(str)
    categoryChanged = Signal(str)
    urlChanged = Signal(str)
    priceChanged = Signal(float)
    availabilityChanged = Signal(int)
    imageChanged = Signal(Path)

    def __init__(self, title, category, url, price, availability, image, parent=None):
        super().__init__(parent)
        self._title = title
        self._category = category
        self._url = url
        self._price = price
        self._availability = availability
        self._image = image

    def get_title(self):
        return self._title

    def set_title(self, title):
        if self._title != title:
            self._title = title
            self.titleChanged.emit(title)

    title = property(get_title, set_title)

    def get_category(self):
        return self._category

    def set_category(self, category):
        if self._category != category:
            self._category = category
            self.categoryChanged.emit(category)

    category = property(get_category, set_category)

    def get_url(self):
        return self._url

    def set_url(self, url):
        if self._url != url:
            self._url = url
            self.urlChanged.emit(url)

    url = property(get_url, set_url)

    def get_price(self):
        return self._price

    def set_price(self, price):
        if self._price != price:
            self._price = price
            self.priceChanged.emit(price)

    price = property(get_price, set_price)

    def get_availability(self):
        return self._availability

    def set_availability(self, availability):
        if self._availability != availability:
            self._availability = availability
            self.availabilityChanged.emit(availability)

    availability = property(get_availability, set_availability)

    def get_image(self):
        return self._image

    def set_image(self, image):
        if self._image != image:
            self._image = image
            self.imageChanged.emit(image)

    image = property(get_image, set_image)


class Category:
    def __init__(self, title, books_list, parent=None):
        super().__init__(parent)
        self._title = title
        self._books_list = books_list

    def add_book(self, book):
        self.books_list.append(book)

    def get_books_list(self):
        return self._books_list

    def set_books_list(self, books_list):
        if self._books_list != books_list:
            self._books_list = books_list

    books_list = property(get_books_list, set_books_list)


class Library:
    def __init__(self, categories):
        self.categories = categories

    def add_category(self, category):
        self.categories.append(category)
