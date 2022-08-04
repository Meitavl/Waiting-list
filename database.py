import mysql.connector


class Db:

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345678",
        database="maccabi"
    )

    def __init__(self, table=None) -> None:
        self.my_cursor = self.mydb.cursor(buffered=True)
        self.table = table

        # self.my_cursor.execute('CREATE DATABASE maccabi')
        # self.my_cursor.execute('SHOW DATABASES')

    def insert_to_table(self, data: tuple) -> None:
        sql_stuff = f'INSERT INTO {self.table}(year, month, day, hour) VALUES (%s, %s, %s, %s)'
        self.my_cursor.execute(sql_stuff, data)
        self.mydb.commit()

    def create_table(self, table: str) -> None:
        self.drop_table(table)
        self.table = table
        self.my_cursor.execute(f'CREATE TABLE {self.table}(Year INTEGER(5), Month INTEGER(10), Day INTEGER(3), Hour VARCHAR(10))')
        self.my_cursor.execute('SHOW TABLES')

    def drop_table(self, table) -> None:
        sql_stuff = f'DROP TABLE IF EXISTS {table}'
        self.my_cursor.execute(sql_stuff)
        self.table = None

    def show_table(self) -> list:
        self.my_cursor.execute(f'SELECT * FROM {self.table}')
        return self.my_cursor.fetchall()

    def show_all_table(self) -> list:
        self.my_cursor.execute('SHOW TABLES')
        return self.my_cursor.fetchall()

    def filter(self, cond) -> list:
        self.my_cursor.execute(f'SELECT * FROM {self.table} WHERE {cond}')
        return self.my_cursor.fetchall()

    def __repr__(self) -> str:
        return f'Table: {self.table}'


db = Db(table='macc')
db.create_table('macc')
# db.drop_table('test')
# for row in db.filter('day > 15'):
#     print(row)
