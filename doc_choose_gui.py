import time
from tkinter import *
import sel
import threading
import csv
import sys
from datetime import datetime as dt
import settings
from dateutil.relativedelta import relativedelta


class ChooseGui:

    def __init__(self, tmp, driver):
        self.root = Tk()
        self.root.title('Waitting list')

        self.entry = {}
        self.button = {}
        self.label = {}
        self.thread = {}

        self.driver = driver

        for ind, item in enumerate(tmp):
            self.doc_choose(ind+1, item.text, command=lambda index=ind+1: self.index_return(index))
        # Shut down
        self.new_button('quit', 20, 0, 'יציאה', command=self.shut_down)


        self.root.mainloop()


    def new_entry(self, name, row, col, show='', state=NORMAL):
        self.entry[name] = Entry(self.root, width=30, show=show, state=state)
        self.entry[name].grid(row=row, column=col, pady=5, padx=5)

    def new_button(self, name, row, col, text, **kwargs):
        self.button[name] = Button(self.root, width=30, text=text)
        for key in kwargs:
            self.button[name][key] = kwargs[key]
        self.button[name].grid(row=row, column=col, columnspan=1)

    def new_label(self, name, row, col, text):
        self.label[name] = Label(self.root, width=30, text=text)
        self.label[name].grid(row=row, column=col)

    def doc_choose(self, *args, **kwargs):
        self.new_button(args[0], args[0], 0, args[1], command=kwargs['command'])


    def index_return(self, index):
        self.doc_index = index
        self.root.destroy()

    def information(self, **kwargs):
        for key in kwargs:
            self.entry[key].config(state=NORMAL)
            self.entry[key].delete(0, END)
            self.entry[key].insert(0, kwargs[key])
            self.entry[key].config(state=DISABLED)

    def stop(self):
        self.button['stop'].config(state=DISABLED)
        self.button['start'].config(state=NORMAL)


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
    for row in load_data(file_name)[0:row_num + 1]:
        print(*row)


def main():

    root = ChooseGui()


if __name__ == '__main__':
    main()
