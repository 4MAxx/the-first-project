import keyboard, time, datetime, random
from dataclasses import Tickets_data

# Класс вывода вывода на консоль общего пользования
class Output:
    # Наименование всплывающих предупреждений
    txt_err = '!!! ОШИБКА !!!\n'
    txt_war = 'ПРЕДУПРЕЖДЕНИЕ !\n'
    txt_suc = 'УСПЕХ !\n'

    @staticmethod
    def clear():
        print("\n" * 50)

    @staticmethod
    def press_enter():
        print(input('Нажмите клавишу Enter для продолжения...'))
        # print('Нажмите клавишу Enter для продолжения...')
        # keyboard.wait('Enter')

    @staticmethod
    def menu(menu):
        n = 1
        len_menu = len(menu)
        while n != len_menu:
            Output.clear()
            for i in range(1, len_menu + 1):
                print(f'{i} - {menu[i][1]}')
            print('Введите вариант:')
            n = keyboard.read_key(True)
            time.sleep(0.2)  # задержка 0,2 секунды
            if n.isdigit():
                n = int(n)
                if n == len_menu:
                    break
                elif n < 1 or n > len_menu:
                    continue
                Output.clear()
                menu.get(n)[0]()
            else:
                n = 1
                continue

    # Метод вывода на консоль квитанций (требуется и для класса админки и для пользовательского класса)
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
            Output.print_ticket(i)


# Классы типов техники
class Tech:
    typ = ''
    def __init__(self, mark='', dam=''):
        if mark == '': self.mark = input(f'Введите марку {self.typ}а: ')
        else: self.mark = mark
        if dam == '': self.damage = input(f'Введите поломку {self.typ}а: ')
        else: self.damage = dam

class Phone(Tech):
    typ = 'телефон'
    def __init__(self, mark='', dam='', os=''):
        super().__init__(mark, dam)
        if os == '': self.os = input('Введите операционную систему: ')
        else: self.os = os

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.os,self.damage])

class Note(Phone):
    typ = 'ноутбук'
    def __init__(self, mark='', dam='', os='', year=''):
        super().__init__(mark, dam, os)
        if year == '': self.year = input(f'Введите год выпуска {self.typ}а: ')
        else: self.year = year

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.os,self.year,self.damage])

class TV(Tech):
    typ = 'телевизор'
    def __init__(self, mark='', dam='', diag=''):
        super().__init__(mark, dam)
        if diag == '': self.diag = input(f'Введите диагональ {self.typ}а: ')
        else: self.diag = diag

    def __str__(self):
        return '-'.join([self.typ,self.mark,self.diag,self.damage])


# Класс пользовательских задач
class User:

    @staticmethod
    def user_give():
        ticket = {'num': '', 'fio': '', 'type': '', 'date_in': str(datetime.date.today()),
                  'date_out': str(datetime.date.today() + datetime.timedelta(days=random.randint(1, 5))), 'status': ''}
        Output.clear()
        print('Регистрация ремонта')
        ticket['num'] = str(Tickets_data.nums + 1)
        ticket['fio'] = input('Введите ФИО: ')
        print('Какой тип техники сдается в ремонт?:')
        print('1 - телефон')
        print('2 - ноутбук')
        print('3 - телевизор')
        t = input()
        if t == '1': ticket['type'] = Phone()
        elif t == '2': ticket['type'] = Note()
        elif t == '3': ticket['type'] = TV()
        ticket['status'] = 'принята в ремонт'
        Output.clear()
        print('Техника принята в ремонт\n')
        Output.print_ticket(ticket)
        ticket['status'] = 'ремонтируется'
        Tickets_data.add_ticket(ticket)
        Tickets_data.save_file()
        Output.press_enter()

    @staticmethod
    def user_get_info():
        k = input('Введите номер квитанции или ФИО:\n')
        Output.clear()
        list_of_found_ticket = Tickets_data.search_ticket(k, 'all')
        if list_of_found_ticket:
            Output.print_tickets(list_of_found_ticket)
        else:
            print(Output.txt_err + 'Квитанция не найдена')
        Output.press_enter()