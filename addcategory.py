from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import connect



class Main:
    def __init__(self):
        self.root = Toplevel()
        self.root.geometry("900x700")
        self.root.config(background="#2B2B2B")

        self.mainLabel = Label(self.root, text="Add Category", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
        self.f.pack(pady=10)

        font = ('calibri', 14)

        self.lb1 = Label(self.f, text="Enter Name", font=font,bg="#333333", fg="white")
        self.inpt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.inpt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = Label(self.f, text="Enter Description", font=font,bg="#333333", fg="white")
        self.inpt2 = Text(self.f, font=font, width=30, height=5, fg="#343638", bg="white")
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.inpt2.grid(row=1, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text="Submit", font=font, command=self.submitForm, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.btn.pack(pady=20)

        self.root.mainloop()


    def submitForm(self):
        name = self.inpt1.get()
        description = self.inpt2.get("1.0",'end-1c') #The first part, "1.0" means that the input should be read from line one, character zero. END is an imported constant which is set to the string "end".

        if len(name) == 0 or len(description) == 0:
            msg.showwarning("Warning", "Please Enter Valid Details.", parent=self.root)
        else:
            conn = connect()

            q = f"insert into category values('{name}', '{description}')"

            cr = conn.cursor()
            cr.execute(q)
            conn.commit()

            msg.showinfo("Success", "New Category has been Added.", parent=self.root)

            self.inpt1.delete(0, 'end')
            self.inpt2.delete("1.0","end")


if __name__ == "__main__":
    Main()