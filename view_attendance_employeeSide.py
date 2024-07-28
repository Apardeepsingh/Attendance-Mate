from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect
from tkcalendar import Calendar, DateEntry
import datetime

class Main:
    def __init__(self, emp_id):
        self.emp_id = emp_id
        # self.root = Tk()
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='Your Attendance Record', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        font = ('calibri', 14)

        self.lb1 = Label(self.f, text="Search Attendance", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = DateEntry(self.f, font=font, width=28, state="readonly", date_pattern='yyyy-MM-dd')
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14), command=lambda: self.searchMessage(""), borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)
        self.inpt.bind('<Return>', self.searchMessage)

        self.attendanceTable = ttk.Treeview(self.root, columns=('id','date','time', 'type'))
        self.attendanceTable.pack(pady=10, padx=20, expand=True, fill='both')

        self.attendanceTable.heading('id', text='ID')
        self.attendanceTable.heading('date', text='Date')
        self.attendanceTable.heading('time', text="Time")
        self.attendanceTable.heading('type', text='Type')

        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.attendanceTable['show'] = 'headings'
        self.getValues()




        self.root.mainloop()


    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()

    
    def searchMessage(self, event):
        text = self.inpt.get()

        q = f"select id, date, time, type from attendance where emp_id={self.emp_id} and date = '{text}'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.attendanceTable.get_children():
            self.attendanceTable.delete(k)
            
        for i in data:
            self.attendanceTable.insert('', index=0, values=i)


    def getValues(self):
        self.conn = connect()

        q = f"select id, date, time, type from attendance where emp_id={self.emp_id}"

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.attendanceTable.get_children():
            self.attendanceTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.attendanceTable.insert('', index=0, values=i)



if __name__ == "__main__":
    Main(9)