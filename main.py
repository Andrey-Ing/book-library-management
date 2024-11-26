"""
Модуль предоставляет точку входа в программу через класс Menu.
Этот класс также содержит главное меню библиотеки, через которое
осуществляется выбор основных действий с книгами.
"""

from command_line_sub_menu import SubMenu
from custom_string import CustomString


class Menu(SubMenu):
    """
    Класс Menu предоставляет систему управления для выбора действий с библиотекой.
    """

    def __init__(self):
        super().__init__()
        self.cs = CustomString()
        self.text_welcome = "Добро пожаловать в систему управления библиотекой!"  # выводится при запуске программы
        self.valid_selection_symbol = ('a', 'd', 'f', 'p', 's', 'q')  # допустимые символы для выбора
        self.choice_message = f"\tдобавление книги\t'{self.cs.choose(self.valid_selection_symbol[0])}'\n" \
                              f"\tудаление книги\t'{self.cs.choose(self.valid_selection_symbol[1])}'\n" \
                              f"\tпоиск книги\t'{self.cs.choose(self.valid_selection_symbol[2])}'\n" \
                              f"\tотображение всех книг\t'{self.cs.choose(self.valid_selection_symbol[3])}'\n" \
                              f"\tизменение статуса книги\t'{self.cs.choose(self.valid_selection_symbol[4])}'\n" \
                              f"\tвыход из программы\t'{self.cs.choose_special(self.valid_selection_symbol[5])}'\n"
        self.invalid_message = "Не понял выбор!"  # при выборе недопустимой команды

    def run_menu(self):
        """Запускает цикл выбора команды и вызова подменю"""
        print(self.cs.welcome(menu.text_welcome))
        choice = ''
        while choice != self.valid_selection_symbol[5]:
            print(self.cs.info("Доступны следующие команды библиотеки,\n"
                               "введите соответствующий символ для выбора:"))
            while True:
                choice = input(self.choice_message)

                if choice in self.valid_selection_symbol:
                    break
                else:
                    print(self.cs.warning(f'{self.invalid_message}'))

            if choice == self.valid_selection_symbol[0]:
                self.add_book()
            elif choice == self.valid_selection_symbol[1]:
                self.delete_book()
            elif choice == self.valid_selection_symbol[2]:
                self.find_book()
            elif choice == self.valid_selection_symbol[3]:
                self.print_all_books()
            elif choice == self.valid_selection_symbol[4]:
                self.change_status()
            elif choice == self.valid_selection_symbol[5]:
                break
            else:
                break


if __name__ == '__main__':
    menu = Menu()
    menu.run_menu()
