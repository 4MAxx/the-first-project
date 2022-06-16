import csv, bcrypt
from datetime import date
import configparser

# Класс управления данными админов
class Admins_data:
    filename = 'Data/admins.csv'        # имя файла с админами  (по дефолту)
    info = []                           # в атрибут загружается список админов (список списков)
    amount = 0                          # количество админов в списке (определяется при загрузке из файла)
    changes = 0                         # маркер изменения списка админов (меняется при редактировании)
    found_ticket = []                   # фиксируется найденная квитанция при действиях с квитанциями (список словарей)
    # found_index = 0

    # мастер логин, дает возможность входа в админ-панель, при отсутствии файла с администраторами,
    # нельзя проверять наличие файла, и при отсутствии давать доступ по первому входу любого логина-пароля
    # иначе можно получить доступ к админ-панели, удалив файл с логинами
    __master_login = []

    @staticmethod                           # загрузка данных админов из файла (список списков)
    def load_file(admins_filename=filename):
        Admins_data.filename = admins_filename
                                            # Загрузка мастер-логина из файла конфигурации
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')
        Admins_data.__master_login = [config['master_login']['login'],
                                      config['master_login']['psw'],
                                      config['master_login']['fio']]
        try:
            with open(Admins_data.filename, 'r', encoding='utf-8') as f_read:
                fr = csv.reader(f_read, delimiter=",")
                Admins_data.info = list(fr)
                Admins_data.amount = len(Admins_data.info)
        except FileNotFoundError:
            Admins_data.info = []
            Admins_data.amount = 0

    @staticmethod                           # запись данных админов в файл
    def save_file():
        with open(Admins_data.filename, 'w', encoding='utf-8') as f_write:
            wr = csv.writer(f_write, lineterminator='\r')
            for i in Admins_data.info:
                wr.writerow(i)

    @staticmethod                           # Сравниваем введенный пароль с хэшем из базы админов
    def compare(psw, hashed):
        try:
            result = bcrypt.checkpw(psw.encode(), hashed.encode())
        except:
            return False
        return result

    @staticmethod                           # Проверяем правильность введенных данных (логин,пароль) при логине админа
    def check_login(l, p):
        if l == Admins_data.__master_login[0] and Admins_data.compare(p, Admins_data.__master_login[1]):
            return True
        else:
            for i in Admins_data.info:
                if l == i[0] and Admins_data.compare(p, i[1]):
                    return True
        return False

    @staticmethod               # Поиск логина в базе (проверка при регистрации админа, исключить дубли логина админов)
    def login_search(log):
        for index in range(0, Admins_data.amount):
            if log == Admins_data.info[index][0]: return index
            index += 1
        return -1  # если возвращается -1, значит логина нету, иначе возвращается индекс логина в списке

    @staticmethod
    def delete_admin(index):                # удаление админа из базы
        Admins_data.info.pop(index)
        Admins_data.amount -= 1             # исправлено в версии 2.3
        Admins_data.changes += 1

    @staticmethod                           # хэширование пароля админа
    def hashed(p):
        return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

    @staticmethod                           # добавление админа в базу
    def add_admin(log, psw, fio):
        Admins_data.info.append([log, Admins_data.hashed(psw), fio])
        Admins_data.changes += 1
        Admins_data.amount += 1

    @staticmethod                           # изменение даты выдачи квитанции
    def change_date(y, m, d):
        Admins_data.found_ticket[0]['date_out'] = str(date(y, m, d))

    @staticmethod                           # изменение статуса квитанции
    def change_status(st):
        Admins_data.found_ticket[0]['status'] = st

    @staticmethod                           # сохранение изненений в базу админов (в файл) при выходе из админ панели
    def save_admins_changes():
        Admins_data.save_file()
        Admins_data.changes = 0

    @staticmethod
    def undo_admins_changes():              # не сохранение изменений при выходе из админ панели
        Admins_data.changes = 0


# Класс управления квитанциями
class Tickets_data:
    filename = 'Data/tickets.csv'       # имя файла с квитанциями (по дефолту)
    data = []                           # в атрибут загружается каитанции (список словарей)
    nums = 0                            # количество загруженных квитанций (определяется при загрузке из файла)
                                        # используется для присвоения следующего номера при регистрации нового ремонта

    found_tickets = []                  # сохраняется наеденные по запросу квитанции (список словарей сортированный)
    found_index = 0                     # индекс найденной квитанции (исп-ся при дейстаиях с квитанциями в админ панели)

    @staticmethod                           # поиск квитанции(ий) с заданными параметрами
    def search_ticket(param, flag):
        # функция поиска квитанций по параметру (номеру или фио - определяется автоматически)
        # если по номеру квитанция нашлась, то запоминается ФИО из этой квитанции,
        # и происходит поиск (рекурсия) по всей базе квитанций с этим ФИО (поиск по заданию)
        # используется set() для исключения дублей при рекурсивном поиске по ФИО и квитанцией найденной по номеру,
        # с флагом 'one' - ищет только номер, 'all' - поиск и номера и всех квитанций с одним ФИО
        def search(k, f='one'):
            s = set()
            if k.isdigit():
                key = 'num'
            else:
                key = 'fio'
            index = 0
            for i in Tickets_data.data:
                if i[key] == k:
                    s.add(tuple(i.items()))
                    if key == 'num':
                        Tickets_data.found_index = index    # запоминаем индекс найденной квитанции (используется
                        break                               # при изменения статуса и даты в админ панели (действия)
                index += 1
            if key == 'num' and s and f == 'all': s.update(search(i['fio']))
            return s  # возвращается сет с кортежами всех найденных квитанций (поиск по номеру и по фио) без повторов

        search = list(search(param, flag))
        if search:
            # преобразование сета кортежей в список словарей как адаптер к функции search
            new_set = []
            for i in search:
                new_set.append(dict(i))
            # Сортировка списка словарей по номеру квитанции (если нужно, то меняем по другому признаку)
            new_s_sorted = sorted(new_set, key=lambda x: x['num'])
            Tickets_data.found_tickets = new_s_sorted
            return new_s_sorted         # Возвращается список словарей найденныйх квитанций (сортированный)
        return 0                        # Возвращается 0 если не найдено квитанций с заданным параметром

    @staticmethod                       # сохранение квитанции (используется в админ панели (действия)
    def save_ticket(list_of_ticket_to_save):
        Tickets_data.data[Tickets_data.found_index] = list_of_ticket_to_save
        Tickets_data.save_file()

    @staticmethod                       # добавление квитанции в data (при регистрации ремонта =Сдать в ремонт=)
    def add_ticket(ticket):
        Tickets_data.data.append(ticket)
        Tickets_data.nums += 1
        Tickets_data.save_file()

    @staticmethod                       # запись базы квитанций в файл
    def save_file():
        with open(Tickets_data.filename, 'w', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(Tickets_data.data[0].keys()), lineterminator='\r')
            writer.writeheader()
            for d in Tickets_data.data:
                writer.writerow(d)

    @staticmethod                       # загрузка данных квитанций из файла
    def load_file(tickets_filename=filename):
        Tickets_data.filename = tickets_filename
        try:
            with open(Tickets_data.filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                Tickets_data.data = []
                for dict in reader:
                    Tickets_data.data.append(dict)
                    Tickets_data.nums += 1
        except FileNotFoundError:
            # если нет файла квитанций, то ошибки при чтении из файла игнорим, есть возможность войти в систему и
            # сдавать в ремонт, админ панель доступна. При попытках поиска информации выводится ошибка, что квитанции нету
            # оно логично - т.к. списки будут пусты
            pass
