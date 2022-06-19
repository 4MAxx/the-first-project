import sys, keyboard
from stuff import normdate
from pynput import keyboard as kb


# Класс вывода в консоль информации о квитанции(ях) (требуется и для класса админки и для пользовательского класса)
class Print_ticket:
    @staticmethod                                   # Вывод в консоль информации об 1 квитанции
    def print_ticket(ticket):
        print(f'Квитанция # {ticket["num"]}:')
        print(f'ФИО:          {ticket["fio"]}')
        print(f'Техника:      {ticket["type"]}')
        print(f'Дата приемки: {normdate(str(ticket["date_in"]))}')
        print(f'Дата выдачи:  {normdate(str(ticket["date_out"]))}')
        print(f'Статус:       {ticket["status"]}')

    @staticmethod                                   # Вывод в консоль информации о квитанциях (много)
    def print_tickets(list_of_tickets):
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
            #     if key == kb.Key.esc:
            #         return False

            with kb.Listener(on_release=on_release) as listener:
                listener.join()
            return k
        return input_ver_1()    # input_ver_2()

    @staticmethod                                   # Метод маскировки звездочками *** при вводе пароля
    def input_psw(prompt):
        pwd = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            key = keyboard.read_key(True)
            # keyboard.unhook_all()
            if key == 'enter':                  # При вводе Enter
                if pwd != '':
                    sys.stdout.write('\n')
                    # print(pwd)
                    return pwd
            if key == 'backspace':              # При вводе Backspace
                if len(pwd) > 0:
                    # Стираем предыдущий символ
                    sys.stdout.write('\b' + ' ' + '\b')
                    sys.stdout.flush()
                    pwd = pwd[:-1]
            if key == 'alt':                    # Имитация смены раскладки (пока не пригодилось)
                keyboard.send('alt+shift')
            else:
                # Маскируем введенные символы
                char = keyboard.read_key(True)
                sys.stdout.flush()
                if len(char) == 1:
                    sys.stdout.write('*')
                    sys.stdout.flush()
                    pwd = pwd + char

    # Альтернативный метод маскировки ввода пароля (есть проблемки)
    # @staticmethod
    # def read_char():
    #     class Pwd:
    #         pwd = ''
    #     def on_press(key):
    #         transit_table = {'<96>': '0', '<97>': '1', '<98>': '2', '<99>': '3', '<100>': '4', '<101>': '5',
    #                          '<102>': '6', '<103>': '7', '<104>': '8', '<105>': '9'}
    #
    #         try:
    #             # Маскируем введенные символы
    #             char = key.char.replace("'", "")
    #             sys.stdout.write('\b' + '*')
    #             sys.stdout.flush()
    #             Pwd.pwd = Pwd.pwd + char
    #         except AttributeError:
    #             if str(key) in transit_table.keys():
    #                 char = transit_table[str(key)]
    #                 sys.stdout.write('\b' + '*')
    #                 sys.stdout.flush()
    #                 Pwd.pwd = Pwd.pwd + char
    #             elif key == kb.Key.enter:
    #                 if Pwd.pwd != '':
    #                     sys.stdout.write('\n')
    #                     sys.stdout.flush()
    #                 return False
    #             elif key == kb.Key.backspace:
    #                 if len(Pwd.pwd) > 0:
    #                     # Стираем предыдущий символ
    #                     sys.stdout.write('\b' + ' ' + '\b')
    #                     sys.stdout.flush()
    #                     Pwd.pwd = Pwd.pwd[:-1]
    #         return True
    #
    #     with kb.Listener(on_press=on_press) as listener:
    #         listener.join()
    #
    #     return Pwd.pwd

    # @staticmethod
    # def input_psw(prompt):
    #     sys.stdout.write(prompt)
    #     sys.stdout.flush()
    #     pwd = Output.read_char()
    #     return pwd

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