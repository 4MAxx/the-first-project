import pymysql
import pymysql.cursors
import configparser
import bcrypt
from datetime import date
import datetime as dtime
from dataclasses import Admins_data, Tickets_data


class Admins_db:
    def __init__(self):
        self.table_for_admins = 'admins'  # создаем атрибут с названием таблицы админов в БД
        config = configparser.ConfigParser()  # загружаем данные конфигурации из config.ini
        config.read('config.ini', encoding='utf-8-sig')
        try:
            self.mydb = pymysql.connect(
                host=config.get('mysql', 'host'),
                port=int(config.get('mysql', 'port')),
                database=config.get('mysql', 'database'),
                user=config.get('mysql', 'user'),
                passwd=config.get('mysql', 'psw')
            )
            self.cur = self.mydb.cursor()
            # логируем результат соединения с БД
            with open(config['log']['log_file'], 'a') as f:
                print(f'{self.table_for_admins} DB connected successfuly... [{dtime.datetime.now()}]', file=f)
        except pymysql.Error as error:
            # логируем результат соединения с БД при неудаче соединения
            with open(config['log']['log_file'], 'a') as f:
                print(f'{self.table_for_admins} DB connection refused... [{dtime.datetime.now()}]\n {error}', file=f)
        # загружаем данные мастер-логина из файла
        self.__master_login = [config['master_login']['login'],
                               config['master_login']['psw'],
                               config['master_login']['fio']]
        # создаем таблицу в БД при ее отсутствии
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_for_admins}'
                         f' (login varchar(50) UNIQUE, psw text, fio text)')
        # определяем количество админов в БД
        self.cur.execute(f'SELECT count(*) FROM {self.table_for_admins}')
        self.amount = self.cur.fetchone()[0]    # количество админов в БД
        self.changes = 0                        # маркер изменения списка админов (меняется при редактировании)
        self.found_ticket = []  # фиксируется найденная квитанция при действиях с квитанциями [{список словарей}]
        self.queries = []       # в этом атрибуте сохраняется история запросов, если придется откатывать изменения

    # загрузка данных админов из файла [[список списков]] не используется
    def load_file(self):
        pass

    # запись данных админов в файл (не используется)
    def save_file(self):
        pass

    # возвращаем все данные админов в виде [[список списков]]
    def getinfo(self):
        self.cur.execute(f'SELECT * FROM {self.table_for_admins}')
        alldata = self.cur.fetchall()
        return [list(x) for x in alldata]

    # Сравниваем введенный пароль с хэшем из базы админов
    def compare(self, psw, hashed):
        try:
            result = bcrypt.checkpw(psw.encode(), hashed.encode())
        except:
            return False
        return result

    # Проверяем правильность введенных данных (логин,пароль) при логине админа
    def check_login(self, l, p):
        if l == self.__master_login[0] and self.compare(p, self.__master_login[1]):
            return True
        else:
            self.cur.execute(f'SELECT * FROM {self.table_for_admins} WHERE login = %s', l)
            alldata = self.cur.fetchone()
            if alldata and self.compare(p, alldata[1]):
                return True
        return False

    # Поиск логина в базе (проверка при регистрации админа / поиск при удалении)
    def login_search(self, log):
        self.cur.execute(f'SELECT * FROM {self.table_for_admins} WHERE login = %s', str(log))
        alldata = self.cur.fetchone()
        if alldata:
            return log  # для работы с БД нужено возвращать не индекс а сам логин админа для удаления
        return -1  # если возвращается -1, значит логина нету

    # удаление админа из базы (с сохранением для отмены изменений)
    def delete_admin(self, log):
        self.cur.execute(f'SELECT * FROM {self.table_for_admins} WHERE login = %s', str(log))
        alldata = self.cur.fetchone()
        # сохраняем обратный запрос в список queries для восстановления в случае отмены изменений
        self.queries.append(f'INSERT INTO {self.table_for_admins} VALUES {alldata}')
        # удаляем запись логина из БД
        self.cur.execute(f'DELETE FROM {self.table_for_admins} WHERE login = (%s)', (str(log),))
        self.mydb.commit()
        self.amount -= 1
        self.changes += 1

    # хэширование пароля админа
    def hashed(self, p):
        return bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()

    # добавление админа в БД>
    def add_admin(self, log, psw, fio):
        # сохраняем обратный запрос в список queries для восстановления в случае отмены изменений
        self.queries.append(f'DELETE FROM {self.table_for_admins} WHERE login = "{log}"')
        # добавляем запись логина в БД
        self.cur.execute(f'INSERT INTO {self.table_for_admins} VALUES (%s,%s,%s)', (log, self.hashed(psw), fio))
        self.mydb.commit()
        self.changes += 1
        self.amount += 1

    def set_found_ticket(self, fTicket):
        self.found_ticket = fTicket

    def get_found_ticket(self):
        return self.found_ticket

    # изменение даты выдачи квитанции
    def change_date(self, y, m, d):
        self.found_ticket[0]['date_out'] = str(date(y, m, d))

    # изменение статуса квитанции
    def change_status(self, st):
        self.found_ticket[0]['status'] = st

    # сохранение изненений в БД при выходе из админ панели
    def save_admins_changes(self):
        self.queries = []
        self.changes = 0

    # отмена изменений при выходе из админ панели
    def undo_admins_changes(self):
        for i in self.queries[::-1]:  # откатываем в обратном порядке, по принципу FIFO
            self.cur.execute(i)  # применяем все сохраненные обратные запросы к БД чтобы откатить все изменения
            self.mydb.commit()
        self.queries = []
        self.changes = 0
        self.update_amount()  # обновляем количество админов в БД

    # сихронизация БД с данными которые записаны в файле (дополняем БД) (служебный метод для заполнения БД вначале)
    def synchronize(self):
        Admins_data.load_file()
        # преобразуем [[список списков]] данных админов в [(список кортежей)] перед записью в БД
        admins = [tuple(x) for x in Admins_data.getinfo()]
        for i in admins:
            try:  # обрабатываем ситуации когда логин уже записан в БД
                self.cur.execute(f'INSERT INTO {self.table_for_admins} VALUES (%s,%s,%s)', i)
                self.mydb.commit()
            except pymysql.Error as error:
                # загружаем данные конфигурации из config.ini
                config = configparser.ConfigParser()
                config.read('config.ini', encoding='utf-8-sig')
                # логируем результат записи с БД при неудаче
                with open(config['log']['log_file'], 'a') as f:
                    print(f'Ошибка при работе с базой данных {self.table_for_admins} [{dtime.datetime.now()}]\n'
                          f' {error}', file=f)
        self.update_amount()  # обновляем количество админов в БД

    # метод определения количества админов в БД (служебный метод)
    def update_amount(self):
        self.cur.execute(f'SELECT count(*) FROM {self.table_for_admins}')
        self.amount = self.cur.fetchone()[0]


class Tickets_db:
    def __init__(self):
        self.table_for_tickets = 'tickets'  # создаем атрибут с названием таблицы квитанций в БД
        config = configparser.ConfigParser()  # загружаем данные конфигурации из config.ini
        config.read('config.ini', encoding='utf-8-sig')
        try:
            self.mydb = pymysql.connect(
                host=config.get('mysql', 'host'),
                port=int(config.get('mysql', 'port')),
                database=config.get('mysql', 'database'),
                user=config.get('mysql', 'user'),
                passwd=config.get('mysql', 'psw')
            )
            self.cur = self.mydb.cursor()
            # логируем результат соединения с БД
            with open(config['log']['log_file'], 'a') as f:
                print(f'{self.table_for_tickets} DB connected successfuly... [{dtime.datetime.now()}]', file=f)
        except pymysql.Error as error:
            # логируем результат соединения с БД при неудаче соединения
            with open(config['log']['log_file'], 'a') as f:
                print(f'{self.table_for_tickets} DB connection refused... [{dtime.datetime.now()}]\n {error}', file=f)
        # создаем таблицу в БД при ее отсутствии
        self.cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_for_tickets}'
                         f' (num varchar(20) UNIQUE, fio text, type text, date_in date,'
                         f' date_out date, status varchar(20))')
        # определяем количество квитанций в БД
        self.cur.execute(f'SELECT count(*) FROM {self.table_for_tickets}')
        self.nums = self.cur.fetchone()[0]  # количество квитанций в БД
        self.found_ticket = []  # фиксируется найденная квитанция при действиях с квитанциями [{список словарей}]
        self.found_index = 0    # "num" найденной квитанции (исп-ся при дейстаиях с квитанциями в админ панели)

    # поиск квитанции(ий) с заданными параметрами
    def search_ticket(self, param, flag):
        # функция поиска квитанций по параметру (номеру или фио - определяется автоматически)
        # если по номеру квитанция нашлась, то запоминается ФИО из этой квитанции,
        # и происходит поиск по БД квитанций с этим ФИО (поиск по заданию)
        # с флагом 'one' - ищет только номер, 'all' - поиск и номера и всех квитанций с одним ФИО
        self.cur = self.mydb.cursor(cursor=pymysql.cursors.DictCursor)
        if param.isdigit():
            key = 'num'
            self.cur.execute(f'SELECT * FROM {self.table_for_tickets} WHERE {key} = %s', str(param))
            alldata = self.cur.fetchall()
            if alldata and flag == 'one':
                self.found_index = alldata[0]['num']  # сохраняем "num" вместо index (разница при работе с БД)
                return alldata
            if alldata and flag == 'all':
                fio = alldata[0]['fio']
                self.cur.execute(f'SELECT * FROM {self.table_for_tickets} WHERE fio = %s', str(fio))
                alldata = self.cur.fetchall()
                return alldata
        else:
            key = 'fio'
            self.cur.execute(f'SELECT * FROM {self.table_for_tickets} WHERE fio = %s', str(param))
            alldata = self.cur.fetchall()
            if alldata:
                return alldata
        return 0

    # обновление квитанции (используется в админ панели (действия) принимается {словарь}
    def update_ticket(self, tic):
        self.cur = self.mydb.cursor()
        self.cur.execute(f'UPDATE {self.table_for_tickets} SET date_out = %s, status = %s WHERE num = %s',
                         (tic['date_out'], tic['status'], self.found_index))
        self.mydb.commit()

    # добавление квитанции в data (при регистрации ремонта =Сдать в ремонт=) приходит {словарь}
    def add_ticket(self, ticket):
        self.cur = self.mydb.cursor()
        self.cur.execute(f'INSERT INTO {self.table_for_tickets} VALUES (%s,%s,%s,%s,%s,%s)', tuple(ticket.values()))
        self.mydb.commit()
        self.nums += 1

    # запись базы квитанций в файл (при работе с БД не используется)
    def save_file(self):
        pass

    # загрузка данных квитанций из файла (при работе с БД не используется)
    def load_file(self):
        pass

    # обновляем количество квитанций
    def update_nums(self):
        self.cur.execute(f'SELECT count(*) FROM {self.table_for_tickets}')
        self.nums = self.cur.fetchone()[0]

    # возвращаем количество квитанций
    def getNums(self):
        return self.nums

    # сихронизация БД с данными которые записаны в файле (дополняем БД) (служебный метод для заполнения БД вначале)
    def synchronize(self):
        Tickets_data.load_file()
        # преобразуем [{список словарей}] в [(список кортежей)] значения (без ключей) перед записью в БД
        tickets = [tuple(x.values()) for x in Tickets_data.getdata()]
        for i in tickets:
            try:  # обрабатываем ситуации когда квитанция уже записана в БД
                self.cur.execute(f'INSERT INTO {self.table_for_tickets} VALUES (%s,%s,%s,%s,%s,%s)', i)
                self.mydb.commit()
            except pymysql.Error as error:
                # загружаем данные конфигурации из config.ini
                config = configparser.ConfigParser()
                config.read('config.ini', encoding='utf-8-sig')
                # логируем результат записи с БД при неудаче
                with open(config['log']['log_file'], 'a') as f:
                    print(f'Ошибка при работе с базой данных {self.table_for_tickets} [{dtime.datetime.now()}]\n'
                          f' {error}', file=f)
        self.update_nums()  # обновляем количество админов в БД


# Блок кода для тестирования работы библиотеки
if __name__ == '__main__':
    base = Tickets_db()

    base.cur.execute("SELECT VERSION()")
    version = base.cur.fetchone()
    print(f"Database version: {version[0]}")
    # base.cur.execute("CREATE DATABASE IF NOT EXISTS project_1st")
    # base.cur.commit()
    # base.cur.execute("SHOW DATABASES")
    # databases = base.cur.fetchall()
    # print(databases)
    # base.synchronize()
    base.cur.close()
