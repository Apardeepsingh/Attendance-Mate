from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import connect

class Main:

    def __init__(self, emp_id):
        self.emp_id = emp_id
        self.root = Toplevel()
        self.root.geometry("900x700")
        self.root.config(background="#2B2B2B")

        self.mainLabel = Label(self.root, text="Change Password", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
        self.f.pack(pady=10)

        font = ('calibri', 14)

        self.lb1 = Label(self.f, text="New Password", font=font,bg="#333333",fg="white")
        self.inpt1 = Entry(self.f, font=font, width=30, show='*', fg="#343638", bg="white")
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.inpt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = Label(self.f, text="Confirm Password", font=font,bg="#333333",fg="white")
        self.inpt2 = Entry(self.f, font=font, width=30, show='*', fg="#343638", bg="white")
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.inpt2.grid(row=1, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text='Update', font=font, command=self.updatePassword, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.btn.pack(pady=20)
        

        self.root.mainloop()



    def updatePassword(self):
        password = self.inpt1.get()
        cpassword = self.inpt2.get()


        if password != cpassword:
            msg.showwarning('Warning',"Passwords don't match", parent=self.root)
        else:
            self.conn = connect()
            q = f"update employee set password='{password}' where id = '{self.emp_id}' "

            self.cr = self.conn.cursor()
            self.cr.execute(q)
            self.conn.commit()

            msg.showinfo("Success", "Your password has been updated", parent=self.root )
            self.root.destroy()