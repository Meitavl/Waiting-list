import time
from tkinter import *
import sel
import threading
import csv
import sys
from datetime import datetime as dt
import settings
from dateutil.relativedelta import relativedelta


class MainGui:

    def __init__(self):
        self.root = Tk()
        self.root.title('Waitting list')
        
        self.entry = {}
        self.button = {}
        self.label = {}
        self.thread = {}
        
        # User name 
        self.new_entry('username', 0, 0)
        self.new_label('username', 0, 1, ':שם משתמש')
        
        # Password
        self.new_entry('password', 1, 0, '*')
        self.new_label('password', 1, 1, ':סיסמה')
        
        # Contact
        self.new_entry('email', 2, 0)
        self.new_label('email', 2, 1, ':אימייל')
        
        # Run button
        self.new_button('start', 3, 1, 'הפעל', command=self.run_button)

        # Stop button
        self.new_button('stop', 3, 0, 'עצור', command=self.stop, state=DISABLED)
        
        # Information
        self.new_entry('running_num', 4, 0, state=DISABLED)
        self.new_label('running_num', 4, 1, ':מספר ריצה')
        self.new_entry('free_queue_num_last', 5, 0, state=DISABLED)
        self.new_label('free_queue_num_last', 5, 1, ':מספר תורים שנמצאו בריצה האחרונה')
        self.new_entry('free_queue_num', 6, 0, state=DISABLED)
        self.new_label('free_queue_num', 6, 1, ':מספר תורים שנמצאו')
        # self.new_entry('breaking_time', 7, 0, state=DISABLED)
        # self.new_label('breaking_time', 7, 1, ':זמן בין ריצות')
        self.new_entry('exception', 8, 0, state=DISABLED)
        self.new_label('exception', 8, 1, ':מספר ריצות שנכשלו')
        self.new_entry('doc_name', 9, 0, state=DISABLED)
        self.new_label('doc_name', 9, 1, ':שם רופא')
        self.new_entry('address', 10, 0, state=DISABLED)
        self.new_label('address', 10, 1, ':שם רופא')
        self.new_entry('start_date', 11, 0, state=DISABLED)
        self.new_label('start_date', 11, 1, ':מתאריך')
        self.new_entry('end_date', 12, 0, state=DISABLED)
        self.new_label('end_date', 12, 1, ':עד תאריך')
        self.new_entry('have_queue', 13, 0, state=DISABLED)
        self.new_label('have_queue', 13, 1, ':האם קיים תור שמור')
        self.new_entry('queue', 14, 0, state=DISABLED)
        self.new_label('queue', 14, 1, ':תור שמור')

        # Shut down
        self.new_button('quit', 20, 0, 'יציאה', command=self.shut_down)

        # Set first queue
        self.new_button('set', 16, 1, 'קביעת תור', command=self.state, bg='red')
        self.new_button('free_list', 16, 0, 'רשימת תורים פנויים', command=lambda: self.open_thread('free_list', print_last_free, args=('doc.csv', 10), daemon=True))

        self.root.mainloop()
     
    def new_entry(self, name, row, col, show='', state=NORMAL):
        self.entry[name] = Entry(self.root, width=30, show=show, state=state)
        self.entry[name].grid(row=row, column=col, pady=5, padx=5)
        
    def new_button(self, name, row, col, text, **kwargs):
        self.button[name] = Button(self.root, width=30, text=text)
        for key in kwargs:
            self.button[name][key] = kwargs[key]
        self.button[name].grid(row=row, column=col, padx=3, pady=3, columnspan=1)
        
    def new_label(self, name, row, col, text):
        self.label[name] = Label(self.root, width=30, text=text)
        self.label[name].grid(row=row, column=col)
        
    def run_button(self):
        username = self.entry['username'].get()
        password = self.entry['password'].get()
        if username == 'admin' or username == 'שגצןמ' or username == '':
            username = settings.id
            password = settings.password
            # self.information(doc_name='קופפר מרגריטה', start_date=dt.today().replace(microsecond=0), end_date=relativedelta(months=1) + dt.today().replace(microsecond=0))
        email = self.entry['email'].get()
        for key in self.entry:
            self.entry[key].config(state=DISABLED)
        save_data('userdata.csv', username, password, email)
        self.thread['selenium'] = (threading.Thread(target=self.start_sel, daemon=True))
        self.thread['selenium'].start()
        self.button['stop'].config(state=NORMAL)
        self.button['start'].config(state=DISABLED)

    def start_sel(self):
        count_miss = 0
        count = 0
        while True:
            exc = ''
            try:
                sel.main(self)

            except:
                exc0, exc1, exc2 = sys.exc_info()
                print(f'{exc0}, {exc1}, {dt.now()}')
                trace_exp(exc2)
                count_miss += 1
                if str(exc1) == 'Wrong id or password':
                    self.stop()
                    self.entry['username'].config(state=NORMAL)
                    self.entry['password'].config(state=NORMAL)
                    self.entry['email'].config(state=NORMAL)
                    break
            count += 1

            self.information(running_num=count, exception=count_miss)
            save_log('log.csv', count, dt.now(), count_miss, exc)
            time.sleep(10)

    def information(self, **kwargs):
        for key in kwargs:
            self.entry[key].config(state=NORMAL)
            self.entry[key].delete(0, END)
            self.entry[key].insert(0, kwargs[key])
            self.entry[key].config(state=DISABLED)

    def stop(self):
        self.button['stop'].config(state=DISABLED)
        self.button['start'].config(state=NORMAL)

    def state(self):
        if self.button['set']['bg'] == 'red':
            self.button['set'].config(bg='green')
            return
        if self.button['set']['bg'] == 'green':
            self.button['set'].config(bg='red')

    def open_thread(self, name, target, daemon, args=None):
        self.thread[name] = threading.Thread(target=target, args=args, daemon=daemon)
        self.thread[name].start()

    def shut_down(self):
        self.root.destroy()


def trace_exp(exc):
    print(exc.tb_frame, exc.tb_lineno)
    save_log('exc_log.csv', dt.now(), exc.tb_frame, exc.tb_lineno)
    if exc.tb_next is None:
        return
    trace_exp(exc.tb_next)


def save_data(file_name, *args):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(args)


def save_log(file_name, *args):
    with open(file_name, 'a') as f:
        writer = csv.writer(f)
        if args[0] == 1:
            heading = ('Count', 'Time', 'Count miss', 'Exception')
            writer.writerow(heading)
        writer.writerow(args)


def load_data(file_name: str) -> list:
    with open(file_name, 'r') as fp:
        reader = csv.reader(fp)
        return list(reader)


def print_last_free(file_name, row_num):
    for row in load_data(file_name)[0:row_num+1]:
        print(*row)


def main():
    root = MainGui()
    

if __name__ == '__main__':
    main()
