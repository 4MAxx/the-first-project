import keyboard, time, csv

class Admins_data:
    info = []
    changes = 0


# -Администраторская панель-
def admin_panel():
    print('\n')
    l = input('Введите логин: ')
    p = input('Введите пароль: ')
    Admins_data.info = read_file(admins_filename)
    if check_login(l, p, Admins_data.info):
        vivod_menu(admin_menu)
    else:
        print(txt_err+'Введенные данные не верны')
        press_enter()
    if Admins_data.changes >= 1:
        admin_save_changes()

def admin_save_changes():
    yes = {'y', 'Y', 'Н', 'н'}
    no = {'n', 'N', 'т', 'Т'}
    while True:
        clear()
        print(txt_war)
        print('Список администраторов был редактирован')
        print('Хотите сохранить изменения? (y/n):')
        key = keyboard.read_key()
        if key in yes:
            with open(admins_filename, 'w', encoding='utf-8') as f_write:
                wr = csv.writer(f_write, lineterminator='\r')
                for i in Admins_data.info:
                    wr.writerow(i)
            Admins_data.changes = 0
            clear()
            print(txt_suc+'Изменения внесены успешно!')
            press_enter()
            break
        elif key in no:
            Admins_data.changes = 0
            break

def check_login(l, p, admins):
    for i in admins:
        if l == i[0] and p == i[1]: return True
    return False

def admin_spisok():
    clear()
    n = 1
    for i in Admins_data.info:
        print(n,' |', ', '.join(i))
        n += 1
    press_enter()

def admin_del():
    clear()
    n = input('Введите логин админа для его удаления: ')
    if len(Admins_data.info) > 1:
        if admin_login_seaarch(n) != -1:
            Admins_data.info.pop(admin_login_seaarch(n))
            Admins_data.changes += 1
            print(txt_suc+'Удаление произошло успешно!')
            press_enter()
        else:
            print(txt_err+' Искомый логин не найден')
            press_enter()
    else:
        print(txt_war+'Удаление единственного админа невозможно')
        press_enter()

def admin_add():
    while True:
        clear()
        print('Регистрация нового администратора')
        log = input('Введите логин: ')
        if admin_login_seaarch(log) == -1:
            psw = input('Введите пароль: ')
            fio = input('Введите ФИО: ')
            Admins_data.info.append([log, psw, fio])
            Admins_data.changes += 1
            break
        else:
            print(txt_err+'Введенный логин уже существует')
            press_enter()
            continue

def admin_login_seaarch(log):
    for index in range(0, len(Admins_data.info)):
        if log == Admins_data.info[index][0]: return index
        index += 1
    return -1   # если возвращается -1, значит логина нету, иначе возвращается индекс логина в списке

def admin_actions():
    k = input('Введите номер квитанции')
    vivod_menu(admin_actions_menu)

def admin_change_status():
    pass

def admin_change_date():
    pass

def admin_get_info():
    pass

# Меню -пользователя-
def user_give():
    pass

def user_get_info():
    pass

# Основные функции -Main-
def vivod_menu(menu):
    n = 1
    while n != len(menu):
        clear()
        for i in range(1, len(menu) + 1):
            print(f'{i} - {menu[i][1]}')
        # n = input('Введите вариант:')
        print('Введите вариант:')
        n = str(keyboard.read_key())
        time.sleep(0.2)                 # задержка 0,1 секунды иначе read_key() считывает дважды
        if n.isdigit():
            n = int(n)
            if n == len(menu): break
            elif n < 1 or n > len(menu): continue
            clear()
            menu.get(n)[0]()
        else:
            n = 1
            continue

def clear():
    print("\n" * 50)

def press_enter():
    print(input('Нажмите клавишу Enter для продолжения...'))

def read_file(name):
    with open(name, 'r', encoding='utf-8') as f_read:
        fr = csv.reader(f_read, delimiter=",")
        return list(fr)

# Менюшки
main_menu = {1:[user_give, 'Сдать в ремонт'],
             2:[user_get_info, 'Просмотреть информацию'],
             3:[admin_panel, 'Зайти в администраторскую панель'],
             4:[0, 'Выход']}

admin_menu = {1:[admin_spisok, 'Отобразить список всех админов'],
              2:[admin_del, 'Удалить админа из списка'],
              3:[admin_add, 'Добавить нового админа'],
              4:[admin_actions, 'Действия с квитанциями'],
              5:[0, 'Выход из администраторской панели']}

admin_actions_menu = {1:[admin_change_status, 'Изменить статус ремонта'],
                      2:[admin_change_date, 'Изменить дату выполнения ремонта'],
                      3:[admin_get_info, 'Посмотреть информацию о квитанции'],
                      4:[0, 'Возврат в администраторскую панель']}

# Приставка текста всплывающих предупреждений
txt_err = '!!! ОШИБКА !!! '
txt_war = 'ПРЕДУПРЕЖДЕНИЕ ! '
txt_suc = 'УСПЕХ ! '

admins_filename = 'Data/admins.csv'



# Тело программы
vivod_menu(main_menu)