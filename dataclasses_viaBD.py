import pymysql
import configparser


class Admins_data:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini', encoding='utf-8-sig')
        try:
            self.mydb = pymysql.connect(
                host=config.get('mysql', 'host'),
                port=int(config.get('mysql', 'port')),
                user=config.get('mysql', 'user'),
                passwd=config.get('mysql', 'psw')
            )
            self.cur = self.mydb.cursor()
            print('BD connected successfuly...')
        except:
            print('BD connection refused...')

