import csv
import re

import database
from email_send import send_email
from datetime import datetime as dt


def data_comp_func(num_res: int) -> (list, dt, dt):
    db = database.Db()
    # for table in db.show_all_table():
    #     print(table[0])

    db.table = 'macc'
    # for date in db.show_table():
    #     print(date)
    with open('userdata.csv') as f:
        reader = list(csv.reader(f))[2]
        end_date = dt.strptime(reader[2], '%Y-%m-%d %H:%M:%S')
        start_date = dt.strptime(reader[1], '%Y-%m-%d %H:%M:%S')
        today = dt.today()
        if today > start_date:
            start_date = today
    return db.filter(f'month<={end_date.month} AND month >= {start_date.month} Limit {num_res}'), end_date, start_date


def compare() -> None:
    free, end_date, start_date = data_comp_func(20)
    msg_head = 'We found free queue:\n'
    msg = ""
    if len(free) > 0:
        for line in free:
            tmp = ''
            line = re.findall('[0-9:]+', str(line))
            for word in line:
                tmp += word + '-'
            time = dt.strptime(tmp, '%Y-%m-%d-%H:%M-')
            if end_date.date() >= time.date() >= start_date.date():
                msg += f'Date: {str(time.date())}, Time: {str(time.time())}\n'
        if len(msg) > 1:
            msg = msg_head + msg
            send_email('meitav.livne@gmail.com', msg)
            # print(f'{msg}Time: {dt.now()}')
        else:
            pass
        # print(f'Sorry there is not free queue yet: {dt.now()}')
    else:
        print(f'Sorry there is not free queue yet: {dt.now()}')
    return

