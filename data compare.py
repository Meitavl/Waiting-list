import database

db = database.Db()
# for table in db.show_all_table():
#     print(table[0])

db.table = 'macc'
for date in db.show_table():
    print(date)
