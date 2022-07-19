import mysql.connector


class Db:

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345678",
        database="maccabi"
    )

    def __init__(self, table=None):
        self.my_cursor = self.mydb.cursor(buffered=True)
        self.table = table

        # my_cursor.execute('CREATE DATABASE maccabi')
        # my_cursor.execute('SHOW DATABASES')

    def insert_to_table(self, data):
        # self.create_table(self.table)
        sql_stuff = f'INSERT INTO {self.table}(year, month, day, hour) VALUES (%s, %s, %s, %s)'
        self.my_cursor.execute(sql_stuff, data)
        self.mydb.commit()

    def create_table(self, table):
        self.drop_table(table)
        self.table = table
        self.my_cursor.execute(f'CREATE TABLE {self.table}(Year INTEGER(5), Month VARCHAR(10), Day INTEGER(3), Hour VARCHAR(10))')
        self.my_cursor.execute('SHOW TABLES')

    def drop_table(self, table):
        sql_stuff = f'DROP TABLE IF EXISTS {table}'
        self.my_cursor.execute(sql_stuff)
        self.table = None

    def show_table(self):
        self.my_cursor.execute(f'SELECT * FROM {self.table}')
        return self.my_cursor.fetchall()

    def show_all_table(self):
        self.my_cursor.execute('SHOW TABLES')
        return self.my_cursor.fetchall()

    def filter(self, cond):
        self.my_cursor.execute(f'SELECT * FROM {self.table} WHERE {cond}')
        return self.my_cursor.fetchall()

    def __repr__(self):
        return f'Table: {self.table}'


db = Db(table='macc')
# db.create_table('macc')
# db.drop_table('test')
# for row in db.filter('day > 15'):
#     print(row)
