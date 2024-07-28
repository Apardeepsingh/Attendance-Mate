from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect


class Main():
    def __init__(self):
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='View Messages', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        self.lb1 = Label(self.f, text="Search Message", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = Entry(self.f, width=30, font=('arial', 14))
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14), command=self.searchMessage, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff" )
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff" )
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)

        self.messageTable = ttk.Treeview(self.root, columns=('id', 'emp_id', 'emp_name', 'title','description', 'date','time'))
        self.messageTable.pack(pady=10, padx=20, expand=True, fill='both')

        self.messageTable.heading('id', text='ID')
        self.messageTable.heading('emp_id', text='Employee ID')
        self.messageTable.heading('emp_name', text='Employee Name')
        self.messageTable.heading('title', text='Title')
        self.messageTable.heading('description', text="Message")
        self.messageTable.heading('date', text='Date')
        self.messageTable.heading('time', text='Time')

        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.messageTable['show'] = 'headings'
        self.getValues()

        self.root.mainloop()

    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()

    
    def searchMessage(self):
        text = self.inpt.get()

        q = f"select messages.id, messages.emp_id, employee.name, messages.title, messages.description, messages.date, messages.time from messages inner join employee on  messages.emp_id=employee.id where title like '%{text}%' or description like '%{text}%' or employee.name like '%{text}%'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.messageTable.get_children():
            self.messageTable.delete(k)
            
        for i in data:
            self.messageTable.insert('', index=0, values=i)


    def getValues(self):

        self.conn = connect()

        q = f"select messages.id, messages.emp_id, employee.name, messages.title, messages.description, messages.date, messages.time from messages inner join employee on  messages.emp_id=employee.id "

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.messageTable.get_children():
            self.messageTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.messageTable.insert('', index=0, values=i)


if __name__ == "__main__":
    Main()