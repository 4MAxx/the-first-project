from user_n_output import Output, User, mystr
from dataclasses import Admins_data, Tickets_data

# Класс интерфейса и функционала Админ-панели
class Adminka:
    temp_login = ''     # при успешном входе сохраняется логин админа (используется при выводе заголовка меню)

                                                # Ветка =АДМИН-ПАНЕЛЬ=
    @staticmethod
    def admin_panel():
        # функция процедуры сохранения изменений списка админов, если список редактировали (удаляли, добавляли)
        def admin_save_changes():
            yes = {'y', 'Y', 'Н', 'н'}
            no = {'n', 'N', 'т', 'Т'}
            while True:
                Output.clear()
                print(Output.txt_war + 'Список администраторов был редактирован')
                print('Хотите сохранить изменения? (y/n):')
                key = Output.readkey()
                if key in yes:
                    Admins_data.save_admins_changes()
                    Output.clear()
                    print(Output.txt_suc + 'Изменения внесены успешно!')
                    Output.press_enter()
                    break
                elif key in no:
                    Admins_data.undo_admins_changes()
                    break

        Admins_data.load_file()
        Output.clear()
        l = input('Введите логин: ')
        p = input('Введите пароль: ')
        if Admins_data.check_login(l, p):
            Adminka.temp_login = l
                                            # вход / выход  =АДМИН-ПАНЕЛЬ=
            Output.menu(Menu_Trees.admin_menu, f'Вы вошли под логином: < {Adminka.temp_login} >')
            Adminka.temp_login = ''
        else:
            print(Output.txt_err+'Введенные данные не верны')
            Output.press_enter()
        if Admins_data.changes >= 1:
            admin_save_changes()            # Если менялся список админов, то проводим процедуру сохранения изменений

    @staticmethod
    def no_admins():
        print(Output.txt_war+'Не зарегистрировано ни одного администратора')

    @staticmethod                           # Вывод в консоль списка админов
    def admin_spisok():
        Output.clear()
        if Admins_data.amount == 0: Adminka.no_admins()
        else:
            n = 1
            for i in Admins_data.info:
                print(n,' |', ', '.join([i[0], i[2]]))
                n += 1
        Output.press_enter()

    @staticmethod                           # Метод удаления админа (запрет на удаление единственного админа)
    def admin_del():
        Output.clear()
        if Admins_data.amount == 0: Adminka.no_admins()
        else:
            n = input('Введите логин админа для его удаления: ')
            if Admins_data.amount > 1:
                ad_log = Admins_data.login_search(n)  # поиск логина в списке, возвращается индекс, если нету -1
                if ad_log != -1:
                    Admins_data.delete_admin(ad_log)
                    print(Output.txt_suc+'Удаление произошло успешно!')
                else:
                    print(Output.txt_err+'Искомый логин не найден')
            else:
                print(Output.txt_war+'Удаление единственного админа невозможно')
        Output.press_enter()

    @staticmethod                           # Метод добавления админа
    def admin_add():

        def check_psw(psw, psw2):           # Функция проверки пароля на соответствие требованиям безопасности
            # Test 1                        # Возвращает либо True, либо текст ошибки
            if '123' in psw or 'password' in psw:
                return 'Пароль слишком простой!'
            # Test 2
            if psw != psw2:
                return 'Введенные пароли различаются'
            # Test 3
            up = 0
            low = 0
            symb_str = '%@#$&*!~'
            digit = 0
            symb = 0
            for i in psw:
                if i.isupper(): up += 1
                if i.islower(): low += 1
                if i.isdigit(): digit += 1
            for i in symb_str:
                symb += psw.count(i)
            # Main test
            if up >= 1 and up + low >= 3 and digit >= 1 and symb >= 1 and 6 <= len(psw):
                return True
            else:
                return 'Пароль не соответствует требованиям безопасности!'


        while True:                         # Тело метода
            Output.clear()
            print('Регистрация нового администратора')
            log = mystr('')                                 # оборачиваем новым классом mystr(), наследованный от str()
                                                            # класс mystr() имеет адаптированные методы проверки
            # Препятствуем вводу пустого логина (должны быть данные)
            log = mystr(input('Введите логин: '))
            if log.is_empty():
                continue
            # Проверка логина на наличие в базе админов
            if Admins_data.login_search(log) == -1:         # продолжаем регистрацию, если такого логина нету в базе
                # Проверяем пароль на соответствие безопасности
                while True:
                    print('\nТребования к паролю, минимум: 1 цифра, 1 заглавная, 1 спец-символ (%@#$&*!~), 6 разрядов')
                    psw = input('Введите пароль: ')
                    psw2 = input('Подтвердите пароль: ')
                    check = check_psw(psw, psw2)
                    if check_psw(psw, psw2) == True:        # Если пароль соответствует требованиям, проходим дальше
                        flag_pass = True
                        break
                    else:
                        print(Output.txt_err + check)       # Вывод в консоль текста ошибки не соответствия пароля
                        Output.press_enter()
                        Output.clear()
                        flag_pass = False               # Если пароль не соответствует, начинаем регистрацию сначала
                        break

                if flag_pass:
                    fio = mystr('')
                    # Препятствуем вводу пустого ФИО (должны быть не пустые данные, в которых не должно быть цифр)
                    while not fio.is_valid():
                        fio = mystr(input('Введите ФИО: '))

                    # После всех проверок записываем данные нового админа в базу
                    Admins_data.add_admin(log, psw, fio)
                    print(Output.txt_suc+'Регистрация администратора произошла успешно')
                    print(f'Логин:{log}, ФИО: {fio}')
                    Output.press_enter()
                    break
            else:
                print(Output.txt_err+'Введенный логин уже существует')
                Output.press_enter()
                continue

                                        # Ветка =админ-панели= \ =ДЕЙСТВИЯ С КВИТАНЦИЯМИ=
    @staticmethod
    def admin_actions():
        Output.clear()
        k = input('Введите номер квитанции:\n')
        list_of_found_tickets = Tickets_data.search_ticket(k, 'one')
        if list_of_found_tickets:
            Admins_data.found_ticket = list_of_found_tickets
                                                                            # вход/выход =ДЕЙСТВИЯ С КВИТАНЦИЯМИ=
            Output.menu(Menu_Trees.admin_actions_menu,
                        f'Квитанция # {k} - {Admins_data.found_ticket[0]["fio"]} '
                        f'(срок: {Admins_data.found_ticket[0]["date_out"]}) - {Admins_data.found_ticket[0]["status"]}')
            Tickets_data.save_ticket(Admins_data.found_ticket[0])       # сохраняем квитанцию в базу в любом случае
        else:
            print(Output.txt_err + 'Квитанция не найдена')
            Output.press_enter()

    @staticmethod                           # Метод изменения статуса квитанции (дейстаия с квитанциями)
    def admin_change_status():
        Output.clear()
        statuses = {1: 'ремонтируется', 2: 'готово', 3: 'выдано клиенту'}
        print('Измените статус ремонта на:')
        print('1 - ремонтируется')
        print('2 - готово')
        print('3 - выдано клиенту')
        t = input()
        try:
            Admins_data.change_status(statuses[int(t)])
            Output.clear()
            print(Output.txt_suc + 'Квитанция после изменения:\n' + Output.txt_line)
            Adminka.admin_get_info()
        except:
            print(Output.txt_err+'Неверный выбор')
            Output.press_enter()

    @staticmethod                           # Метод изменения даты ремонта (дейстаия с квитанциями)
    def admin_change_date():
        Output.clear()
        print('Производится изменение даты выполнения ремонта:')
        try:
            d = int(input('Введите число (ЧЧ):\n'))
            m = int(input('Введите месяц (ММ):\n'))
            y = input('Введите год (ГГГГ):\n')
            if len(y) < 4:                  # Если год введен не 4-мя цифрами, то вызывается ошибка
                raise ValueError
            else:
                y = int(y)
            Admins_data.change_date(y, m, d)
            Output.clear()
            print(Output.txt_suc + 'Квитанция после изменения:\n' + Output.txt_line)
            Adminka.admin_get_info()
        except:
            print(Output.txt_err + 'Ошибка ввода даты')
            Output.press_enter()


    @staticmethod                           # Вывод в консоль информации о квитанции
    def admin_get_info():
        Output.print_ticket(Admins_data.found_ticket[0])
        Output.press_enter()


# Менюшки
class Menu_Trees():
    main_menu = {1:[User.user_give, 'Сдать в ремонт'],
                 2:[User.user_get_info, 'Просмотреть информацию'],
                 3:[Adminka.admin_panel, 'Зайти в администраторскую панель'],
                 0:[0, 'Выход']}

    admin_menu = {2:[Adminka.admin_spisok, 'Отобразить список всех админов'],
                  3:[Adminka.admin_del, 'Удалить админа из списка'],
                  4:[Adminka.admin_add, 'Добавить нового админа'],
                  1:[Adminka.admin_actions, 'Действия с квитанциями'],
                  0:[0, 'Выход из администраторской панели']}

    admin_actions_menu = {3:[Adminka.admin_change_status, 'Изменить статус ремонта'],
                          2:[Adminka.admin_change_date, 'Изменить дату выполнения ремонта'],
                          1:[Adminka.admin_get_info, 'Посмотреть информацию о квитанции'],
                          0:[0, 'Возврат в администраторскую панель']}


# Тело программы
Tickets_data.load_file()
Output.menu(Menu_Trees.main_menu)