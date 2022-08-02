import csv

import database

db = database.Db()
# for table in db.show_all_table():
#     print(table[0])

db.table = 'macc'
# for date in db.show_table():
#     print(date)
with open('userdata.csv') as f:
    reader = list(csv.reader(f))[2]
    print(reader)
    end_date = int(reader[2][5:7])
    start_date = int(reader[1][5:7])
    print(end_date, start_date)
for date in db.filter(f'month<={end_date} AND month > {start_date} Limit 5'):
    print(date)
