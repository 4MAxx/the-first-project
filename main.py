import keyboard, time, csv, datetime, random

# -Администраторская панель-
class Admins_data:
    info = []
    amount = 0
    changes = 0
    found_ticket = {}
    found_index = 0
    # мастер логин, дает возможность входа в админ-панель, при отсутствии файла с администраторами,
    # нельзя проверять наличие файла, и при отсутствии давать доступ по первому входу любого логина-пароля
    # иначе можно получить доступ к админ-панели, удалив файл с логинами
    master_login = [['master', '123', 'master login']]

    @staticmethod
    def load_file(name):
        try:
            with open(name, 'r', encoding='utf-8') as f_read:
                fr = csv.reader(f_read, delimiter=",")
                Admins_data.info = list(fr)
                Admins_data.amount = len(Admins_data.info)
        except FileNotFoundError:
            Admins_data.info = []
            Admins_data.amount = 0

    @staticmethod
    def save_file(name):
        with open(name, 'w', encoding='utf-8') as f_write:
            wr = csv.writer(f_write, lineterminator='\r')
            for i in Admins_data.info:
                wr.writerow(i)

def admin_panel():
    Admins_data.load_file(admins_filename)
    print('\n')
    l = input('Введите логин: ')
    p = input('Введите пароль: ')
    if check_login(l, p, Admins_data.info) or check_login(l, p, Admins_data.master_login):
        vivod_menu(admin_menu)
    else:
        print(txt_err+'Введенные данные не верны')
        press_enter()
    if Admins_data.changes >= 1:
        admin_save_changes()

def check_login(l, p, admins):
    for i in admins:
        if l == i[0] and p == i[1]: return True
    return False

def admin_save_changes():
    yes = {'y', 'Y', 'Н', 'н'}
    no = {'n', 'N', 'т', 'Т'}
    while True:
        clear()
        print(txt_war+'Список администраторов был редактирован')
        print('Хотите сохранить изменения? (y/n):')
        key = keyboard.read_key()
        if key in yes:
            Admins_data.save_file(admins_filename)
            Admins_data.changes = 0
            clear()
            print(txt_suc+'Изменения внесены успешно!')
            press_enter()
            break
        elif key in no:
            Admins_data.changes = 0
            break

def if_no_admins():
    print(txt_war+'Не зарегистрировано ни одного администратора')

def admin_spisok():
    clear()
    if Admins_data.amount == 0: if_no_admins()
    else:
        n = 1
        for i in Admins_data.info:
            print(n,' |', ', '.join(i))
            n += 1
    press_enter()

def admin_del():
    clear()
    if Admins_data.amount == 0: if_no_admins()
    else:
        n = input('Введите логин админа для его удаления: ')
        if len(Admins_data.info) > 1:
            if admin_login_search(n) != -1:
                Admins_data.info.pop(admin_login_search(n))
                Admins_data.changes += 1
                print(txt_suc+'Удаление произошло успешно!')
            else:
                print(txt_err+'Искомый логин не найден')
        else:
            print(txt_war+'Удаление единственного админа невозможно')
    press_enter()

def admin_add():
    while True:
        clear()
        print('Регистрация нового администратора')
        log = input('Введите логин: ')
        if admin_login_search(log) == -1:
            psw = input('Введите пароль: ')
            fio = input('Введите ФИО: ')
            Admins_data.info.append([log, psw, fio])
            Admins_data.changes += 1
            Admins_data.amount += 1
            break
        else:
            print(txt_err+'Введенный логин уже существует')
            press_enter()
            continue

def admin_login_search(log):
    for index in range(0, len(Admins_data.info)):
        if log == Admins_data.info[index][0]: return index
        index += 1
    return -1   # если возвращается -1, значит логина нету, иначе возвращается индекс логина в списке

def admin_actions():
    k = input('Введите номер квитанции:\n')
    Admins_data.found_ticket = from_SetTup_to_ListDict(search_ticket(k, 'one'))[0]
    if len(Admins_data.found_ticket):
        Tickets_data.load_file(ticket_filename)
        vivod_menu(admin_actions_menu)
        Tickets_data.save_ticket()
    else:
        print(txt_err + 'Квитанция не найдена')
        press_enter()


def admin_change_status():
    print('Измените статус ремонта на:')
    print('1 - ремонтируется')
    print('2 - готово')
    print('3 - выдано клиенту')
    t = input()
    if t == '1':
        Admins_data.found_ticket['status'] = 'ремонтируется'
    elif t == '2':
        Admins_data.found_ticket['status'] = 'готово'
    elif t == '3':
        Admins_data.found_ticket['status'] = 'выдано клиенту'
    clear()
    print(txt_suc + 'Квитанция после изменения:\n-----')
    admin_get_info()

def admin_change_date():
    print('Производится изменение даты выполнения ремонта:')
    d = int(input('Введите число:\n'))
    m = int(input('Введите месяц:\n'))
    y = int(input('Введите год:\n'))
    Admins_data.found_ticket['date_out'] = datetime.date(y, m, d)
    clear()
    print(txt_suc+'Квитанция после изменения:\n-----')
    admin_get_info()

def admin_get_info():
    print_ticket(Admins_data.found_ticket)
    press_enter()

def admin_save_ticket_changes():
    pass


# Класс управления квитанциями
class Tickets_data:
    data = []
    nums = 0
    found_tickets = []
    found_index = 0

    def save_ticket():
        Tickets_data.data[Tickets_data.found_index] = Admins_data.found_ticket
        Tickets_data.save_file(ticket_filename)

    @staticmethod
    def save_file(name):
        with open(name, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(Tickets_data.data[0].keys()), lineterminator='\r')
            writer.writeheader()
            for d in Tickets_data.data:
                writer.writerow(d)

    @staticmethod
    def load_file(name):
        with open(name, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            Tickets_data.data = []
            for dict in reader:
                Tickets_data.data.append(dict)
                Tickets_data.nums += 1


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


# Меню -пользователя
def user_give():
    ticket = {'num': '', 'fio': '', 'type': '', 'date_in': datetime.date.today(),
              'date_out': datetime.date.today() + datetime.timedelta(days=random.randint(1, 5)), 'status': ''}
    clear()
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
    clear()
    print('Техника принята в ремонт\n')
    print_ticket(ticket)
    ticket['status'] = 'ремонтируется'
    Tickets_data.data.append(ticket)
    Tickets_data.nums += 1
    Tickets_data.save_file(ticket_filename)
    press_enter()

def print_ticket(ticket):
    print(f'Квитанция # {ticket["num"]}:')
    print(f'ФИО:          {ticket["fio"]}')
    print(f'Техника:      {ticket["type"]}')
    print(f'Дата приемки: {ticket["date_in"]}')
    print(f'Дата выдачи:  {ticket["date_out"]}')
    print(f'Статус:       {ticket["status"]}')

def user_get_info():
    k = input('Введите номер квитанции или ФИО:\n')
    clear()
    Tickets_data.found_tickets = from_SetTup_to_ListDict(search_ticket(k, 'all'))
    if len(Tickets_data.found_tickets):
        for i in Tickets_data.found_tickets:
            print_ticket(i)
        press_enter()
    else:
        print(txt_err + 'Квитанция не найдена')
        press_enter()

def from_SetTup_to_ListDict(s):
    new_s = []
    for i in list(s):
        new_s.append(dict(i))
    return new_s

def search_ticket(k, flag='one'):
    s = set()
    if k.isdigit(): key = 'num'
    else: key = 'fio'
    index = 0
    for i in Tickets_data.data:
        if i[key] == k:
            s.add(tuple(i.items()))
            if key == 'num':
                Tickets_data.found_index = index
                break
        index += 1
    if key == 'num' and s and flag == 'all': s.update(search_ticket(i['fio']))
    return s


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
txt_err = '!!! ОШИБКА !!!\n'
txt_war = 'ПРЕДУПРЕЖДЕНИЕ !\n'
txt_suc = 'УСПЕХ !\n'

admins_filename = 'Data/admins.csv'
ticket_filename = 'Data/tickets.csv'


# Тело программы
Tickets_data.load_file(ticket_filename)
vivod_menu(main_menu)
