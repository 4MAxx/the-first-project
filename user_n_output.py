import datetime, random, sys
import keyboard
from dataclasses import Tickets_data
from pynput import keyboard as kb

# Класс вывода в консоль информации о квитанции(ях) (требуется и для класса админки и для пользовательского класса)
class Print_ticket:
    @staticmethod
    def print_ticket(ticket):                       # Вывод в консоль информации об 1 квитанции

        def date_print(date):                       # Нормализация формата Даты к виду ЧЧ-ММ-ГГГГ (при выводе в консоль)
            str = date.split('-')
            return '-'.join(str[::-1])

        print(f'Квитанция # {ticket["num"]}:')
        print(f'ФИО:          {ticket["fio"]}')
        print(f'Техника:      {ticket["type"]}')
        print(f'Дата приемки: {date_print(ticket["date_in"])}')
        print(f'Дата выдачи:  {date_print(ticket["date_out"])}')
        print(f'Статус:       {ticket["status"]}')

    @staticmethod
    def print_tickets(list_of_tickets):             # Вывод в консоль информации о квитанциях (много)
        for i in list_of_tickets:
            Print_ticket.print_ticket(i)


# Класс ввода вывода на консоль общего пользования
class Output(Print_ticket):
    txt_err = '\n!!! ОШИБКА !!!\n'                  # Наименование всплывающих предупреждений
    txt_war = 'ПРЕДУПРЕЖДЕНИЕ !!!\n'
    txt_suc = '\nУСПШНО !!!\n'

    txt_line = '='*35                               # ===================================


    @staticmethod                                   # очистка экрана консоли (своеобразная)
    def clear():
        print("\n" * 50)

    @staticmethod                                   # ожидание ввода клавиши для продолжения работы
    def press_enter():
        print(input('Нажмите клавишу Enter для продолжения...'))
        # print('Нажмите клавишу Enter для продолжения...')
        # keyboard.wait('Enter')

    @staticmethod
    def readkey():                  # Метод для считывания символа с клавиатуры - реагирует при нажатии

        def input_ver_1():          # Вариант ввода с импользованием модуля keyboard и метода read_key
            key = keyboard.read_key(True)
            return key

        def input_ver_2():          # Вариант ввода с импользованием модуля pynput и keyboard.listener

            def on_release(key):
                global k
                k = ''
                transit_table = {'<96>': '0', '<97>': '1', '<98>': '2', '<99>': '3', '<100>': '4', '<101>': '5',
                                 '<102>': '6', '<103>': '7', '<104>': '8', '<105>': '9'}
                try:
                    k = key.char.replace("'", "")
                except AttributeError:
                    if str(key) in transit_table.keys():
                        k = transit_table[str(key)]
                return False

            # def on_release(key):
            #     print(f'Key released: {key}')
            #     if key == keyboard.Key.esc:
            #         return False

            with kb.Listener(on_release=on_release) as listener:
                listener.join()
            return k

        return input_ver_1()    # input_ver_2()

    @staticmethod
    def input_psw(prompt):
        pwd = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            key = keyboard.read_key(True)
            if key == 'enter':                  # При вводе Enter
                if pwd != '':
                    sys.stdout.write('\n')
                    return pwd
            if key == 'backspace':              # При вводе Backspace
                if len(pwd) > 0:
                    # Стираем предыдущий символ
                    sys.stdout.write('\b' + ' ' + '\b')
                    sys.stdout.flush()
                    pwd = pwd[:-1]
            else:
                # Маскируем введенные символы
                char = keyboard.read_key(True)
                if len(char) == 1:
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    pwd = pwd + char

    @staticmethod                                       # Основной цыкл вывода меню в консоль
    def menu(menu, title='Добро пожаловать в мастерскую !'):
        len_menu = len(menu)
        while True:
            Output.clear()
            print(f'{title}\n'+Output.txt_line)         # вывод заголовка меню
            for i in range(1, len_menu):                # вывод меню
                print(f'{i} - {menu[i][1]}')
            print(f'0 - {menu[0][1]}')                  # вывод последнего пунка меню (выход)
            print('\nВведите вариант и нажмите Enter:')
            # n = Output.readkey()
            n = input()                                 # считывание выбора пользователя
            try:
                n = int(n)
                if n == 0:                              # выход при вводе '0'
                    break
                menu.get(n)[0]()                        # запуск функционала согласно выбору
            except:
                pass                                    # цыкл глотает несуществующий выбор


# Классы типов техники
class Tech:
    typ = ''
    def __init__(self, mark='', dam=''):
        if mark == '':
            str = mystr('')
            while str.is_empty():                       # Нельзя ввести пустые данные
                str = mystr(input(f'Введите марку {self.typ}а: '))
            self.mark = str
        else:
            self.mark = mark
        if dam == '':
            str = mystr('')
            while str.is_empty():                       # Нельзя ввести пустые данные
                str = mystr(input(f'Введите поломку {self.typ}а: '))
            self.damage = str
        else:
            self.damage = dam

class Phone(Tech):
    typ = 'телефон'
    def __init__(self, mark='', dam='', os=''):
        super().__init__(mark, dam)
        if os == '':
            str = mystr('')
            while str.is_empty():                       # Нельзя ввести пустые данные
                str = mystr(input('Введите операционную систему: '))
            self.os = str
        else:
            self.os = os

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.os,self.damage])

class Note(Phone):
    typ = 'ноутбук'
    def __init__(self, mark='', dam='', os='', year=''):
        super().__init__(mark, dam, os)
        if year == '':
            str = mystr('')                             # Нельзя ввести пустые данные или не цифры
            while str.is_empty() or not str.isdigit() or len(str) != 4:
                str = mystr(input(f'Введите год выпуска (ГГГГ) {self.typ}а: '))
            self.year = str
        else:
            self.year = year

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.os,self.year,self.damage])

class TV(Tech):
    typ = 'телевизор'
    def __init__(self, mark='', dam='', diag=''):
        super().__init__(mark, dam)
        if diag == '':
            str = mystr('')
            while str.is_empty() or not str.isdigit() or len(str) > 2:      # Нельзя ввести пустые данные или не цифры
                str = mystr(input(f'Введите диагональ {self.typ}а: '))
            self.diag = str
        else:
            self.diag = diag

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.diag,self.damage])


# Класс c методами проверок строк, адаптированные под цели программы на базе класса str()
class mystr(str):
    # Функция проверки на наличие цифр в строке (если хотябы одна есть, то возвращает True)
    def have_digit(self):
        for i in self:
            if i.isdigit():
                return True
        return False

    # Функция проверки на пустотю строку или строку с одними пробелами
    def is_empty(self):
        if not self or self.isspace():
            return True
        return False

    # Функция совмещающая в себя 2 проверки (на пустоту и цифры) - если хоть одна проверка True, то строка не валидна
    def is_valid(self):
        if self.is_empty() or self.have_digit():
            return False
        return True


# Класс пользовательских задач
class User:
    @staticmethod                                       # Функционал при выборе =Сдать технику в ремонт=
    def user_give():
        ticket = {'num': '', 'fio': '', 'type': '', 'date_in': str(datetime.date.today()),
                  'date_out': str(datetime.date.today() + datetime.timedelta(days=random.randint(1, 5))), 'status': ''}
        Output.clear()
        print('Регистрация ремонта\n'+Output.txt_line)
        ticket['num'] = str(Tickets_data.nums + 1)
        ticket['fio'] = mystr(input('Введите ФИО: '))   # оборачиваем новым классом mystr(), наследованный от str()
                                                        # класс mystr() имеет адаптированные методы проверки
        # При условии что ФИО не пустое и не содержит цифры - продолжаем регистрацию
        if ticket['fio'].is_valid():
            print('Какой тип техники сдается в ремонт?:')
            print('1 - телефон')
            print('2 - ноутбук')
            print('3 - телевизор')
            t = input()
            if t and t in '123':
                if t == '1': ticket['type'] = Phone()
                elif t == '2': ticket['type'] = Note()
                elif t == '3': ticket['type'] = TV()
                ticket['status'] = 'принята в ремонт'
                Output.clear()
                print(Output.txt_suc+'Техника принята в ремонт\n'+Output.txt_line)
                Output.print_ticket(ticket)
                ticket['status'] = 'ремонтируется'
                Tickets_data.add_ticket(ticket)
            else:
                print(Output.txt_err + 'Неверный выбор')
        else:
            print(Output.txt_err + 'ФИО не должно быть пустым или содержать цифры')
        Output.press_enter()

    @staticmethod                                       # Функционал при выборе =Просмотреть информацию=
    def user_get_info():
        Output.clear()
        k = input('Введите номер квитанции или ФИО:\n')
        Output.clear()
        list_of_found_ticket = Tickets_data.search_ticket(k, 'all')
        if list_of_found_ticket:
            Output.print_tickets(list_of_found_ticket)
        else:
            print(Output.txt_err + 'Квитанция не найдена')
        Output.press_enter()