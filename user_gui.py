import datetime, random
from stuff import mystr
from dataclasses import Tickets_data as Tickets_dat
from in_n_output import Output
from dataclasses_viaBD import Tickets_db


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


# Класс пользовательских задач
class User:
    mode_flag = 'files'
    @staticmethod                           # Функционал при выборе =СДАТЬ ТЕХНИКУ В РЕМОНТ=
    def user_give():
        # Проверка режима работы с БД или файлами
        if User.mode_flag == 'db':
            Tickets_data = Tickets_db()
        else:
            Tickets_data = Tickets_dat()
        # регистрация ремонта
        ticket = {'num': '', 'fio': '', 'type': '', 'date_in': str(datetime.date.today()),
                  'date_out': str(datetime.date.today() + datetime.timedelta(days=random.randint(1, 5))), 'status': ''}
        Output.clear()
        print('Регистрация ремонта\n'+Output.txt_line)
        ticket['num'] = str(Tickets_data.getNums() + 1)
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

    @staticmethod                           # Функционал при выборе =ПРОСМОТРЕТЬ ИНФОРМАЦИЮ=
    def user_get_info():
        # Проверка режима работы с БД или файлами
        if User.mode_flag == 'db':
            Tickets_data = Tickets_db()
        else:
            Tickets_data = Tickets_dat()

        Output.clear()
        k = input('Введите номер квитанции или ФИО:\n')
        Output.clear()
        list_of_found_ticket = Tickets_data.search_ticket(k, 'all')
        if list_of_found_ticket:
            Output.print_tickets(list_of_found_ticket)
        else:
            print(Output.txt_err + 'Квитанция не найдена')
        Output.press_enter()