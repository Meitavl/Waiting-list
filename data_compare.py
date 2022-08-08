import csv
import re
import database
from datetime import datetime as dt
import main_gui



def data_comp_func(num_res: int, data: main_gui) -> (list, dt, dt):
    db = database.Db()  # Connect to DB
    db.table = 'macc'  # Define table

    end_date = dt.strptime(data.entry['end_date'].get(), '%Y-%m-%d %H:%M:%S')
    start_date = dt.strptime(data.entry['start_date'].get(), '%Y-%m-%d %H:%M:%S')
    today = dt.today()
    if today > start_date:
        start_date = today
    return db.filter(f'month<={end_date.month} AND month >= {start_date.month} Limit {num_res}')


def compare(data: main_gui) -> None:
    free = data_comp_func(20, data)
    msg = 'We found free queue:\n'
    count = 0
    if len(free) > 0:
        for line in free:
            tmp = ''
            line = re.findall('[0-9:]+', str(line))
            for word in line:
                tmp += word + '-'
            time = dt.strptime(tmp, '%Y-%m-%d-%H:%M-')
            start_date = dt.strptime(data.entry['start_date'].get(), '%Y-%m-%d %H:%M:%S')
            end_date = dt.strptime(data.entry['end_date'].get(), '%Y-%m-%d %H:%M:%S')
            if end_date.date() >= time.date() >= start_date.date():
                msg += f'Date: {str(time.date())}, Time: {str(time.time())}\n'
                count += 1

        # send_email('meitav.livne@gmail.com', msg)
        if count == 0:
            print(f'{msg}Time: {dt.now()}')
        if data.entry['free_queue_num'].get() == '':
            sum_count = 0
        else:
            sum_count = int(data.entry['free_queue_num'].get())
        sum_count += count
        data.information(free_queue_num_last=count, free_queue_num=sum_count)
    else:
        print(f'Sorry there is not free queue yet: {dt.now()}')
    return

