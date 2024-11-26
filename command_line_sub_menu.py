"""
Модуль представляет собой набор подменю, которые выбираются в зависимости от
нужных пользователю задач. Подменю поддерживать ввод пользователем данных, через
стандартный ввод и вывод результата. В результате работы подменю производиться и
выполнение необходимых действий с данными в библиотеке.
"""

import books_data_library_control as bc
from custom_string import CustomString


class InputInfoBook:
    """
     Этот класс отвечает за ввод информации о книге от пользователя.
     Ввод и вывод через стандартные input и print.
    """

    def __init__(self):
        # допустимые значения для ввода
        self.title_min_max_length = 1, 200
        self.autor_min_max_length = 1, 100
        self.year_min_max = -7000, 3000
        self.acceptable_status_book = 'i', 'o'
        # сообщения об ошибках которые могут выводиться пользователю
        self.invalid_message = "Не понял ввод!"
        self.invalid_id_message = "Неверный идентификатор! ID должен содержать две буквы, дефис и число"

        self.cs = CustomString()

    def get_title(self) -> str:
        title = str(input("Введите название книги: "))
        while not self.title_min_max_length[0] <= len(title) <= self.title_min_max_length[1]:
            print(f"{self.invalid_message}\n"
                  f"Введите название книги от {self.title_min_max_length[0]} "
                  f"до {self.title_min_max_length[1]} символов")
            title = str(input("Название книги: "))
        return title

    def get_author(self) -> str:
        autor = str(input("Введите автора: "))
        while not self.autor_min_max_length[0] <= len(autor) <= self.autor_min_max_length[1]:
            print(f"{self.invalid_message}\n"
                  f"Введите автора от {self.autor_min_max_length[0]} "
                  f"до {self.autor_min_max_length[1]} символов")
            autor = str(input("Автор: "))
        return autor

    def get_year(self) -> int:
        year = input("Введите год издания: ")
        while not (year.lstrip('-').isdigit() and self.year_min_max[0] <= int(year) <= self.year_min_max[1]):
            print(f"{self.invalid_message}\n"
                  f"Введите год от {self.year_min_max[0]} до {self.year_min_max[1]}")
            year = input("Год издания: ")
        return int(year)

    def get_status(self) -> bool:
        val_in_choose = self.cs.choose(self.acceptable_status_book[0])
        val_out_choose = self.cs.choose(self.acceptable_status_book[1])

        status = input(f"Введите статус книги '{val_in_choose}' (в наличии) или "
                       f"'{val_out_choose}' (выдана): ")
        while status not in self.acceptable_status_book:
            status = input(f"{self.invalid_message}\n"
                           f"Нужно ввести '{val_in_choose}' (в наличии) или "
                           f"'{val_out_choose}' (выдана): ")
        return True if status == self.acceptable_status_book[0] else False

    def get_id(self) -> str:
        id_book = input("Введите ID книги: ")
        while len(id_book) < 4 or not (id_book[:2].isalpha() and id_book[2] == '-' and id_book[3:].isdigit()):
            print(self.cs.warning(self.invalid_id_message))
            id_book = input("Введите ID: ")
        return id_book


class SubMenu(InputInfoBook):
    """
    Этот класс отвечает за обработку подменю и работу с книгами
    и их данными в библиотеке через импортированный модуль

    Методы:
        add_book(): добавляет новую книгу в библиотеку
        delete_book(): удаляет книгу из библиотеки
        find_book(): находит книгу в библиотеке
        print_all_books(): печатает все книги в библиотеке
        print_books_from_id(id_book_list: list): печатает книги из указанного списка идентификаторов
        change_status(): изменяет статус книги (в наличие или выдана)
    """

    def __init__(self):
        super().__init__()

    def add_book(self) -> None:
        book = bc.BookBase(self.get_title(), self.get_author(), self.get_year())
        id_new_book = bc.add_book_in_library(book)
        print(self.cs.good(f"Книга успешно добавлена, ID: {id_new_book}"))

    def delete_book(self) -> bool:
        """Возвращает True, если удаление прошло успешно, иначе False"""
        id_book = self.get_id()
        if bc.delete_book_in_library(id_book):
            print(self.cs.good(f"Книга с ID: {id_book} успешно удалена"))
            return True
        else:
            print(self.cs.warning(f"Книга с ID: {id_book} не удалена (возможно, такой книги не существует)"))
            return False

    def find_book(self) -> list:
        """Возвращает список ID найденных книг"""
        valid_selection_symbol = ('t', 'a', 'y')
        invalid_message = "Не понял выбор!"
        while True:
            choice = input("Для поиска книги:\n"
                           f"\tпо названию введите '{valid_selection_symbol[0]}'\n"
                           f"\tпо автору введите '{valid_selection_symbol[1]}'\n"
                           f"\tпо году введите '{valid_selection_symbol[2]}'\n")

            if choice in valid_selection_symbol:
                break
            else:
                print(self.cs.warning(f'{invalid_message}'))

        print(self.cs.info("Поддерживаются регулярные выражения"))
        id_list = list()
        if choice == valid_selection_symbol[0]:
            title = input("Введите название книги: ")
            id_list = bc.find_book_in_library(title=title)
        elif choice == valid_selection_symbol[1]:
            author = input("Введите автора книги: ")
            id_list = bc.find_book_in_library(author=author)

        elif choice == valid_selection_symbol[2]:
            year = input("Введите год издания: ")
            id_list = bc.find_book_in_library(year=year)

        self.print_books_from_id(id_list)
        print(self.cs.info_result(f"Всего найдено книг: {len(id_list)}"), '\n')
        return id_list

    def print_all_books(self) -> None:
        books_dict = bc.get_all_books_in_library()
        for id_book, book in books_dict.items():
            print(self.cs.separate('*' * 20) + '\n' +
                  f"ID книги:\t" + self.cs.id_book(f'{id_book}') + '\n' +
                  f"Название:\t{book[bc.BookBase.title_idx]}\n" +
                  f"Автор:\t\t{book[bc.BookBase.author_idx]}\n" +
                  f"Год издания:\t{book[bc.BookBase.year_idx]}\n" +
                  self.cs.good('в наличии') if book[bc.BookBase.status_idx] else
                  self.cs.warning('выдана') + '\n')

        print(self.cs.info_result(f"Всего книг в библиотеке: {len(books_dict)}"), '\n')

    def print_books_from_id(self, id_book_list: list) -> None:
        """
        Аргументы:
            id_book_list (list): Список идентификаторов книг для печати
        """
        books_dict = bc.get_all_books_in_library()
        for id_book, book in books_dict.items():
            for id_ in id_book_list:
                if id_ == id_book:
                    print(self.cs.separate('*' * 20) + '\n' +
                          f"ID книги:\t" + self.cs.id_book(f'{id_book}') + '\n' +
                          f"Название:\t{book[bc.BookBase.title_idx]}\n" +
                          f"Автор:\t\t{book[bc.BookBase.author_idx]}\n" +
                          f"Год издания:\t{book[bc.BookBase.year_idx]}\n" +
                          self.cs.good('в наличии') if book[bc.BookBase.status_idx] else
                          self.cs.warning('выдана') + '\n')

    def change_status(self) -> bool:
        """Возвращает True в случае успешного изменения статуса книги,
            False в противном случае"""
        id_book = self.get_id()
        if id_book in bc.get_all_books_in_library():
            current_status = bc.get_book_from_id(id_book).status
            print(f"Текущий статус книги:", self.cs.good('в наличии') if current_status else (
                    self.cs.warning('выдана') + '\n'))
            required_status = self.get_status()
            bc.change_book_status(id_book, required_status)
            print("Оставлено без изменений" if current_status == required_status else
                  self.cs.good("Изменено"))

            return True
        else:
            print(self.cs.warning(f"Книги с ID: {id_book} нет в библиотеке"))
            return False
