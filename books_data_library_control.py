"""
Модуль представляет собой базу данных и обеспечивает систему управления данными
библиотеки книг. Данные представляет собой JSON файл в котором записаны ID, название,
автор книги, а также её наличие в библиотеке. ID генерируется случайным образом
и уникально для каждой книги. Поддерживается добавления, удаления, поиска и изменение
 статуса книг в библиотеке.
"""

import re
from random import randint
import json

storage_books_name = 'books_data_library.json'  # файл уже должен существовать


def get_new_id(books_dict: dict) -> str:
    """
    Генерирует новый уникальный идентификатор для книги состоящий из двух букв, дефиса и
    числа, которое может иметь произвольную длину.

    Аргументы:
    books_dict (dict): Словарь, содержащий существующие книги и их данные.

    Возвращает:
    str: Новый уникальный идентификатор для книги.
    """
    prefix_chr = chr(randint(ord('A'), ord('Z'))) + chr(randint(ord('A'), ord('Z')))
    bias_mul_id = 10
    attempts = 10
    while True:
        bias_mul_id *= 10
        for _ in range(attempts):
            postfix_number = randint(100 * bias_mul_id, 1000 * bias_mul_id)
            new_book_id = prefix_chr + '-' + str(postfix_number)
            if new_book_id not in books_dict:
                return new_book_id


class BookBase:
    """
    Базовое представление книги с возможностью выдачи последовательных данных.
    """

    def __init__(self, title: str, author: str, year: int, status: bool = True):
        self.title = title
        self.author = author
        self.year = year
        self.status = status  # True - на месте в библиотеке, False - выдана

    def get_serial_data(self):
        return [self.title, self.author, self.year, self.status]
    # Для возможности доступа к последовательным данным по индексу
    title_idx = 0
    author_idx = 1
    year_idx = 2
    status_idx = 3


def _library_read_data(filename: str) -> dict:
    """
    Считывает данные из файла JSON.

    Аргументы:
    filename (str): Имя файла для чтения.

    Возвращает:
    dict: Данные, считанные из файла.
    """
    with open(filename, 'r') as stor_r:
        data = json.load(stor_r)
        return data


def _library_save_data(filename: str, data: dict):
    """
    Сохраняет данные в файл JSON.

    Аргументы:
    filename (str): Имя файла для сохранения,
    data (dict): Данные для сохранения.
    """
    with open(filename, 'w') as stor_w:
        json.dump(data, stor_w, indent=4)


def add_book_in_library(book: BookBase) -> str:
    """
    Добавляет книгу в библиотеку.

    Аргументы:
    book (BookBase): Книга для добавления.

    Возвращает:
    str: Уникальны идентификатор добавленной книги.
    """
    data_books = _library_read_data(storage_books_name)
    new_id = get_new_id(data_books)
    data_books[new_id] = book.get_serial_data()
    _library_save_data(storage_books_name, data_books)
    return new_id


def delete_book_in_library(book_id: str) -> bool:
    """
    Удаляет книгу из библиотеки.

    Аргументы:
    book_id (str): Идентификатор книги для удаления.

    Возвращает:
    bool: True, если книга была удалена, False в противном случае.
    """
    data_books = _library_read_data(storage_books_name)
    if book_id in data_books:
        del data_books[book_id]
        _library_save_data(storage_books_name, data_books)
        return True
    else:
        return False


def find_book_in_library(title: str = None, author: str = None, year: str = None) -> list:
    """
    Находит книги в библиотеке по названию, автору и году. Ввод поддерживает
    регулярные выражения. В случае передачи нескольких аргументов, поиск будет
    осуществляться по всем аргументам и будут выданы ID всех книг,
    подходящих по параметрам одного из аргументов.

    Аргументы:
    title (str, необязательно): Название книги для поиска,
    author (str, необязательно): Автор книги для поиска,
    year (str, необязательно): Год книги для поиска/

    Возвращает:
    list: Список идентификаторов найденных книг. Если не найдено ни одной книги
    возвращает пустой список. При ошибке в регулярном выражении возвращает пустой
    список по аргументу с ошибкой, либо найденные книги по остальным аргументам
    """
    result = []
    data_books = _library_read_data(storage_books_name)
    if title is not None:
        for book_id, book in data_books.items():
            try:
                if re.fullmatch(title, book[BookBase.title_idx]):
                    result.append(book_id)
            except re.error:
                break
    if author is not None:
        for book_id, book in data_books.items():
            try:
                if re.fullmatch(author, book[BookBase.author_idx]):
                    result.append(book_id)
            except re.error:
                break
    if year is not None:
        for book_id, book in data_books.items():
            try:
                if re.fullmatch(str(year), str(book[BookBase.year_idx])):
                    result.append(book_id)
            except re.error:
                break

    return result


def get_all_books_in_library() -> dict:
    """
    Возвращает все книги в библиотеке в виде словаря
    """
    return _library_read_data(storage_books_name)


def change_book_status(book_id: str, status: bool) -> bool:
    """
    Изменяет статус книги в библиотеке.

    Аргументы:
    book_id (str): Идентификатор книги, статус которой нужно изменить,
    status (bool): Новый статус книги.

    Возвращает:
    bool: True, если статус был изменен, False в противном случае.
    """
    data_books = _library_read_data(storage_books_name)
    if book_id in data_books:
        data_books[book_id][BookBase.status_idx] = status
        _library_save_data(storage_books_name, data_books)
        return True
    else:
        return False


def get_book_from_id(book_id: str) -> BookBase:
    """
    Получает книгу из библиотеки на основе ее идентификатора.

    Аргументы:
    book_id (str): идентификатор книги, которую нужно получить.

    Возвращает:
    BookBase: книга с указанным идентификатором.

    Вызывает:
    Исключение KeyError: если книга с указанным идентификатором не найдена.
    """
    data_books = _library_read_data(storage_books_name)
    if book_id in data_books:
        book_data = data_books[book_id]
        return BookBase(book_data[BookBase.title_idx],
                        book_data[BookBase.author_idx],
                        book_data[BookBase.year_idx],
                        book_data[BookBase.status_idx])
    else:
        raise (KeyError(f"Book with id {book_id} not found"))
