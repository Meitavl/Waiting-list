import csv
from tkinter import *
from tkcalendar import DateEntry
import datetime as dt
import sel


class Gui1:

    def __init__(self, master, web_page):

        self.web_page = web_page

        self.master = master

        myframe = Frame(master)
        myframe.grid()

        self.doc_entry = Entry(master, width=50)
        self.doc_entry.grid(row=0, column=1, pady=10, padx=10)

        self.doc_list = Listbox(master, width=50)
        self.doc_list.grid(row=1, column=1, pady=10)

        self.my_button = Button(master, text='send', command=self.send)
        self.my_button.grid(row=2, column=1)

        self.date_start = DateEntry(master, selectmode='day')
        self.date_start.grid(row=0, column=0, padx=10)

        self.date_end = DateEntry(master, selectmode='day')
        self.date_end.grid(row=1, column=0)

        self.binding()

    def send(self):
        save_data(self)
        self.master.destroy()
        return

    def clicker(self, e):
        doc_name_list = input_data(self.doc_entry.get(), self.web_page)
        self.list_update(doc_name_list)

    def list_update(self, data):
        self.doc_list.delete(0, END)
        if len(data):
            for item in data:
                if self.doc_entry.get() in item:
                    self.doc_list.insert(END, item)

    def binding(self):

        self.doc_entry.bind("<KeyRelease>", self.clicker)
        self.doc_list.bind("<<ListboxSelect>>", self.fill_entry)


    def fill_entry(self, e):
        if self.doc_list.size() > 0:
            self.doc_entry.delete(0, END)
            self.doc_entry.insert(0, self.doc_list.get(self.doc_list.curselection()))
            self.clicker(e)


def input_data(string, web_page):
    if __name__ == '__main__':
        str_list = ['שובל', 'שיר', 'שובר', 'מיכאל']
        return str_list

    return sel.data_s(string, web_page)


def save_data(gui):

    with open('data.csv', 'w') as f:
        writer = csv.writer(f)
        doc_name = gui.doc_entry.get()
        start_date = gui.date_start.get_date()
        start_date = dt.datetime.fromisoformat(str(start_date))
        end_date = gui.date_end.get_date()
        end_date = dt.datetime.fromisoformat(str(end_date))
        writer.writerow((doc_name, start_date, end_date))


def main(web_page=0):

    app_width = 500
    app_height = 300
    root = Tk()
    root.title('בחירת רופא')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2)+200
    y = (screen_height/2) - (app_height/2)

    root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
    root.lift()
    root.attributes("-topmost", True)

    g = Gui1(root, web_page)
    root.mainloop()


if __name__ == '__main__':
    main()

