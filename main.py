from user_n_output import Output, User
from dataclasses import Admins_data, Tickets_data
import keyboard


class Adminka:

    # Ветка =АДМИН-ПАНЕЛЬ=
    @staticmethod
    def admin_panel():

        def admin_save_changes():
            yes = {'y', 'Y', 'Н', 'н'}
            no = {'n', 'N', 'т', 'Т'}
            while True:
                Output.clear()
                print(Output.txt_war + 'Список администраторов был редактирован')
                print('Хотите сохранить изменения? (y/n):')
                key = keyboard.read_key(True)
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
        print('\n')
        l = input('Введите логин: ')
        p = input('Введите пароль: ')
        if Admins_data.check_login(l, p):
            Output.menu(Menu_Trees.admin_menu)              # вход / выход  =АДМИН-ПАНЕЛЬ=
        else:
            print(Output.txt_err+'Введенные данные не верны')
            Output.press_enter()
        if Admins_data.changes >= 1:
            admin_save_changes()                # Если менялся список админов, то проводим процедуру сохранения изменений

    @staticmethod
    def no_admins():
        print(Output.txt_war+'Не зарегистрировано ни одного администратора')

    @staticmethod
    def admin_spisok():
        Output.clear()
        if Admins_data.amount == 0: Adminka.no_admins()
        else:
            n = 1
            for i in Admins_data.info:
                print(n,' |', ', '.join(i))
                n += 1
        Output.press_enter()

    @staticmethod
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

    @staticmethod
    def admin_add():
        while True:
            Output.clear()
            print('Регистрация нового администратора')
            log = input('Введите логин: ')
            if Admins_data.login_search(log) == -1:
                psw = input('Введите пароль: ')
                fio = input('Введите ФИО: ')
                Admins_data.add_admin(log, psw, fio)
                break
            else:
                print(Output.txt_err+'Введенный логин уже существует')
                Output.press_enter()
                continue


    # Ветка =админ-панели= \ =ДЕЙСТВИЯ С КВИТАНЦИЯМИ=
    @staticmethod
    def admin_actions():
        # Tickets_data.load_file()                                  # загружаем данные квитанций из файла
        k = input('Введите номер квитанции:\n')
        list_of_found_tickets = Tickets_data.search_ticket(k, 'one')
        if list_of_found_tickets:
            Admins_data.found_ticket = list_of_found_tickets        # фиксируем квитанцию для обработки в админ панели
            Output.menu(Menu_Trees.admin_actions_menu)                          # вход/выход =ДЕЙСТВИЯ С КВИТАНЦИЯМИ=
            Tickets_data.save_ticket(Admins_data.found_ticket[0])   # сохраняем изменения квитанции в общий список квитанций
        else:
            print(Output.txt_err + 'Квитанция не найдена')
            Output.press_enter()

    @staticmethod
    def admin_change_status():
        statuses = {1: 'ремонтируется', 2: 'готово', 3: 'выдано клиенту'}
        print('Измените статус ремонта на:')
        print('1 - ремонтируется')
        print('2 - готово')
        print('3 - выдано клиенту')
        t = input()
        try:
            Admins_data.change_status(statuses[int(t)])
            Output.clear()
            print(Output.txt_suc + 'Квитанция после изменения:\n-----')
            Adminka.admin_get_info()
        except:
            print(Output.txt_err+'Неверный выбор')
            Output.press_enter()

    @staticmethod
    def admin_change_date():
        print('Производится изменение даты выполнения ремонта:')
        d = int(input('Введите число (ЧЧ):\n'))
        m = int(input('Введите месяц (ММ):\n'))
        y = int(input('Введите год (ГГГГ):\n'))
        Admins_data.change_date(y, m, d)
        Output.clear()
        print(Output.txt_suc+'Квитанция после изменения:\n-----')
        Adminka.admin_get_info()

    @staticmethod
    def admin_get_info():
        Output.print_ticket(Admins_data.found_ticket[0])
        Output.press_enter()


# Менюшки
class Menu_Trees():
    main_menu = {1:[User.user_give, 'Сдать в ремонт'],
                 2:[User.user_get_info, 'Просмотреть информацию'],
                 3:[Adminka.admin_panel, 'Зайти в администраторскую панель'],
                 4:[0, 'Выход']}

    admin_menu = {1:[Adminka.admin_spisok, 'Отобразить список всех админов'],
                  2:[Adminka.admin_del, 'Удалить админа из списка'],
                  3:[Adminka.admin_add, 'Добавить нового админа'],
                  4:[Adminka.admin_actions, 'Действия с квитанциями'],
                  5:[0, 'Выход из администраторской панели']}

    admin_actions_menu = {1:[Adminka.admin_change_status, 'Изменить статус ремонта'],
                          2:[Adminka.admin_change_date, 'Изменить дату выполнения ремонта'],
                          3:[Adminka.admin_get_info, 'Посмотреть информацию о квитанции'],
                          4:[0, 'Возврат в администраторскую панель']}


# Тело программы
Tickets_data.load_file()
Output.menu(Menu_Trees.main_menu)