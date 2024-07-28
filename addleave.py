from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import connect
from tkcalendar import Calendar, DateEntry
import datetime


class Main:
    def __init__(self, emp_id):
        self.root = Toplevel()
        self.root.geometry("900x700")
        self.root.config(background="#2B2B2B")

        self.mainLabel = Label(self.root, text="Add Leave", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
        self.f.pack(pady=10)

        font = ('calibri', 14)

        self.lb1 = Label(self.f, text="Employee Id", font=font,bg="#333333", fg="white")
        self.inpt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.inpt1.grid(row=0, column=1, padx=10, pady=10)
        self.inpt1.insert(0, emp_id)
        self.inpt1.config(state="readonly")

        self.lb2 = Label(self.f, text="Enter Date", font=font,bg="#333333", fg="white")
        self.inpt2 = DateEntry(self.f, font=font, width=28, state="readonly", date_pattern='yyyy-MM-dd', fg="#343638", bg="white")
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.inpt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3 = Label(self.f, text="Enter Remarks", font=font,bg="#333333", fg="white")
        self.inpt3 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.inpt3.grid(row=2, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text='Submit', font=font, command=self.submitForm,  borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.btn.pack(pady=20)

        self.root.mainloop()


    def submitForm(self):
        empId = self.inpt1.get()
        date = self.inpt2.get()
        message = self.inpt3.get()

        if len(empId)==0 or len(message)==0 or len(date)==0:
            msg.showwarning('Warning', 'Please Enter Valid Details.')
        else:
            conn = connect()

            q = f"insert into leaves values(null, '{date}', '{empId}', '{message}', 'Pending' )"

            cr = conn.cursor()
            cr.execute(q)
            conn.commit()

            msg.showinfo("Success", f"Your Leave has been requested.", parent=self.root )

            self.inpt1.delete(0, 'end')
            self.inpt2.delete(0, 'end')
            self.inpt3.delete(0, 'end')



if __name__ == "__main__":
    Main(8)