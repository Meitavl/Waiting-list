from tkinter import *
import sel
import threading
import csv


class MainGui:

    def __init__(self):
        self.root = Tk()
        self.root.title('Waitting list')
        
        self.entry = {}
        self.button = {}
        self.label = {}
        
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
        sel_thread = threading.Thread(target=self.run_button)
        sel_thread.daemon = True
        self.new_button('run', 3, 0, 'הפעל', sel_thread.start)
        
        # Information
        self.new_entry('running_num', 4, 0, state=DISABLED)
        self.new_label('running_num', 4, 1, ':מספר ריצה')
        self.new_entry('free_queue_num', 5, 0, state=DISABLED)
        self.new_label('free_queue_num', 5, 1, ':מספר תורים שנמצאו:')
        self.new_entry('breaking_time', 6, 0, state=DISABLED)
        self.new_label('breaking_time', 6, 1, ':זמן בין ריצות')
        self.new_entry('exception', 6, 0, state=DISABLED)
        self.new_label('exception', 6, 1, ':מספר ריצות שנכשלו')
        self.new_entry('doc_name', 7, 0, state=DISABLED)
        self.new_label('doc_name', 7, 1, ':שם רופא')
        
        # Shut down
        self.new_button('quit', 8, 0, 'יציאה', self.shut_down)

        self.root.mainloop()
     
    def new_entry(self, name, row, col, show='', state=NORMAL):
        self.entry[name] = Entry(self.root, width=30, show=show, state=state)
        self.entry[name].grid(row=row, column=col, pady=5, padx=5)
        
    def new_button(self, name, row, col, text, command=''):
        self.button[name] = Button(self.root, width=50, text=text, command=command)
        self.button[name].grid(row=row, column=col, columnspan=2)
        
    def new_label(self, name, row, col, text, command=0):
        self.label[name] = Label(self.root, width=30, text=text)
        self.label[name].grid(row=row, column=col)
        
    def run_button(self):
        self.thread = threading.enumerate()
        username = self.entry['username'].get()
        password = self.entry['password'].get()
        email = self.entry['email'].get()
        self.entry['username'].config(state=DISABLED)
        self.entry['password'].config(state=DISABLED)
        self.entry['email'].config(state=DISABLED)
        self.button['run'].config(state=DISABLED)
        save_data('userdata.csv', username, password, email)
        sel.main(self)

    def information(self, running_num, free_queue_num, breaking_time, doc_name):
        for e in self.entry:
            self.entry[e].delete(0, END)
        self.entry['running_num'].insert(0, running_num)
        self.entry['free_queue_num'].insert(0, free_queue_num)
        self.entry['breaking_time'].insert(0, breaking_time)
        self.entry['doc_name'].insert(0, doc_name)

    def shut_down(self):
        self.root.destroy()




def save_data(file_name, *args):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(args)


def load_data(file_name: str) -> list:
    with open(file_name, 'r') as fp:
        reader = csv.reader(fp)
        return list(reader)


def main():
    MainGui()
    

if __name__ == '__main__':
    main()
