import datetime, random
import keyboard
from dataclasses import Tickets_data
from pynput import keyboard as kb

# Методы вывода на консоль квитанций (требуется и для класса админки и для пользовательского класса)
class Print_ticket:
    @staticmethod
    def print_ticket(ticket):

        def date_print(date):
            str = date.split('-')
            return '-'.join(str[::-1])

        print(f'Квитанция # {ticket["num"]}:')
        print(f'ФИО:          {ticket["fio"]}')
        print(f'Техника:      {ticket["type"]}')
        print(f'Дата приемки: {date_print(ticket["date_in"])}')
        print(f'Дата выдачи:  {date_print(ticket["date_out"])}')
        print(f'Статус:       {ticket["status"]}')

    @staticmethod
    def print_tickets(list_of_tickets):
        for i in list_of_tickets:
            Print_ticket.print_ticket(i)


# Класс вывода вывода на консоль общего пользования
class Output(Print_ticket):
    txt_err = '\n!!! ОШИБКА !!!\n'                # Наименование всплывающих предупреждений
    txt_war = 'ПРЕДУПРЕЖДЕНИЕ !!!\n'
    txt_suc = '\nУСПШНО !!!\n'

    txt_line = '='*35


    @staticmethod
    def clear():
        print("\n" * 50)

    @staticmethod
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
            str = ''
            while not str or str.isspace():
                str = input(f'Введите марку {self.typ}а: ')
            self.mark = str
        else:
            self.mark = mark
        if dam == '':
            str = ''
            while not str or str.isspace():
                str = input(f'Введите поломку {self.typ}а: ')
            self.damage = str
        else:
            self.damage = dam

class Phone(Tech):
    typ = 'телефон'
    def __init__(self, mark='', dam='', os=''):
        super().__init__(mark, dam)
        if os == '':
            str = ''
            while not str or str.isspace():
                str = input('Введите операционную систему: ')
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
            str = ''
            while not str or str.isspace():
                str = input(f'Введите год выпуска {self.typ}а: ')
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
            str = ''
            while not str or str.isspace():
                str = input(f'Введите диагональ {self.typ}а: ')
            self.diag = str
        else:
            self.diag = diag

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.diag,self.damage])


# Класс пользовательских задач
class User:
    @staticmethod
    def user_give():
        ticket = {'num': '', 'fio': '', 'type': '', 'date_in': str(datetime.date.today()),
                  'date_out': str(datetime.date.today() + datetime.timedelta(days=random.randint(1, 5))), 'status': ''}
        Output.clear()
        print('Регистрация ремонта\n'+Output.txt_line)
        ticket['num'] = str(Tickets_data.nums + 1)
        ticket['fio'] = input('Введите ФИО: ')
        if ticket['fio'] and not ticket['fio'].isspace():
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
                Output.clear()
                print(Output.txt_err + 'Неверный выбор')
        else:
            print(Output.txt_err + 'ФИО не должно быть пустым')
        Output.press_enter()

    @staticmethod
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