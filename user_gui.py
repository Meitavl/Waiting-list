import csv
from tkinter import *


class Screen:

    def __init__(self, user):

        self.entry = []
        self.label = []
        self.button = []

        self.root = Tk()
        self.root.title(f'{user}')
        self.root.geometry('500x300')

        self.entry_func(0, 1)
        self.entry_func(1, 1)

        self.label_func('User Name:', 0, 0)
        self.label_func('Password:', 1, 0)
        self.button_func('Send', self.send_button, 2, 1)


        self.root.mainloop()

    def entry_func(self, row, col):
        self.entry.append(Entry(self.root, width=50))
        self.entry[-1].grid(padx=10, pady=10, row=row, column=col)

    def label_func(self, line, row, col):
        self.label.append(Label(self.root, text=f'{line}'))
        self.label[-1].grid(padx=10, row=row, column=col)

    def button_func(self, text, com, row, col):
        self.button.append(Button(self.root, text=text, command=com))
        self.button[-1].grid(row=row, column=col)

    def send_button(self):
        userdata = []
        for entry in self.entry:
            userdata.append(entry.get())
        with open('userdata.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(tuple(userdata))
        self.root.destroy()

# user = Screen('user')

# moshe = Screen('moshe')
