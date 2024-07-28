from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import connect
import admin_dashboard


class Main:
    def __init__(self):
        self.root = Toplevel()
        self.root.geometry('900x800')
        self.root.config(background="#2B2B2B")

        self.mainLabel = Label(self.root, text="Admin Login", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
        self.f.pack(pady=10)

        font = ('calibri', 14)

        self.lb1 = Label(self.f, text='Enter Email', font=font,bg="#333333", fg="white")
        self.txt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb1.grid(row=0, column=0, pady=10, padx=10)
        self.txt1.grid(row=0, column=1, pady=10, padx=10)

        self.lb2 = Label(self.f, text='Enter Password', font=font,bg="#333333", fg="white")
        self.txt2 = Entry(self.f, font=font, width=30, show='*', fg="#343638", bg="white")
        self.lb2.grid(row=1, column=0, pady=10, padx=10)
        self.txt2.grid(row=1, column=1, pady=10, padx=10)

        self.btn = Button(self.root, text='Submit', font=font, command=self.verifyAdmin, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.btn.pack(pady=20)


        self.root.mainloop()

    
    def verifyAdmin(self):
        email = self.txt1.get()
        password = self.txt2.get()

        conn = connect()

        q = f"select * from admin where email='{email}' and password='{password}'"

        cr = conn.cursor()
        cr.execute(q)
        data = cr.fetchall()

        if len(data) == 0:
            msg.showerror('Login Failed', 'Invalid Credentials', parent=self.root)
        else:
            msg.showinfo("Success", "Login Successful", parent=self.root)
            self.root.destroy()
            # print(data)
            admin_dashboard.Main(data[0][0])



if __name__ == "__main__":
    Main()