from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import connect, verifyEmail, verifyMobile


class Main:

    def __init__(self):
        self.root = Toplevel()
        self.root.geometry("900x700")
        self.root.config(background="#2B2B2B")

        self.mainLabel = Label(self.root, text="Add Admin", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
        self.f.pack(pady=10)

        font = ('calibri', 14)
        
        self.lb1 = Label(self.f, text="Enter Name", font=font,bg="#333333", fg="white")
        self.inpt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.inpt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = Label(self.f, text="Enter Email", font=font,bg="#333333", fg="white")
        self.inpt2 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.inpt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3 = Label(self.f, text="Enter Mobile", font=font,bg="#333333", fg="white")
        self.inpt3 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.inpt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4 = Label(self.f, text="Select Role", font=font,bg="#333333", fg="white")
        self.inpt4 = ttk.Combobox(self.f, font=font, width=28, state='readonly', values=['Super Admin', 'Admin'])
        # self.inpt4.configure(background="#343638")
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.inpt4.grid(row=3, column=1, padx=10, pady=10)

        self.lb5 = Label(self.f, text="Enter Password", font=font,bg="#333333",fg="white")
        self.inpt5 = Entry(self.f, font=font, width=30, show='*', fg="#343638", bg="white")
        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.inpt5.grid(row=4, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text='Submit', font=font, command=self.submitForm, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.btn.pack(pady=20)
        

        self.root.mainloop()

    def submitForm(self):
        name = self.inpt1.get()
        email = self.inpt2.get()
        mobile = self.inpt3.get()
        role = self.inpt4.get()
        password = self.inpt5.get()


        if len(name)==0 or len(email)==0 or len(mobile)==0 or len(role)==0 or len(password)==0 or mobile.isalpha():
            msg.showwarning('Warning', 'Please Enter Valid Details.')
        else:
            if verifyMobile(mobile) == 'Invalid' or verifyEmail(email) == 'Invalid':
                msg.showwarning('Warning',"Invalid Email or Mobile Number", parent=self.root)
            else:

                conn = connect()

                q = f"insert into admin values(null, '{name}', '{email}', '{mobile}', '{role}', '{password}')"

                cr = conn.cursor()
                cr.execute(q)
                conn.commit()

                msg.showinfo("Success", f"{name} has been added as admin", parent=self.root )

                self.inpt1.delete(0, 'end')
                self.inpt2.delete(0, 'end')
                self.inpt3.delete(0, 'end')
                self.inpt5.delete(0, 'end')
                self.inpt4.set('')

if __name__ == "__main__":
    Main()