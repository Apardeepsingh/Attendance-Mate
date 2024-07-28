from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import connect, verifyEmail, verifyMobile
from tkinter.filedialog import askopenfilename
import cv2, random


class Main:
    def __init__(self):
        self.root = Toplevel()
        # self.root = Tk()
        self.root.geometry("900x700")
        self.root.config(background="#2B2B2B")

        self.mainLabel = Label(self.root, text="Add Employee", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
        self.f.pack(pady=10)

        font = ('calibri', 14)

        self.lb1 = Label(self.f, text="Enter Name", font=font ,bg="#333333", fg="white")
        self.inpt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.inpt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = Label(self.f, text="Enter Father's Name", font=font ,bg="#333333", fg="white")
        self.inpt2 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.inpt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3 = Label(self.f, text="Enter Mobile", font=font ,bg="#333333", fg="white")
        self.inpt3 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.inpt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4 = Label(self.f, text="Enter Email", font=font ,bg="#333333", fg="white")
        self.inpt4 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.inpt4.grid(row=3, column=1, padx=10, pady=10)
        self.inpt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb5 = Label(self.f, text="Enter Address", font=font ,bg="#333333", fg="white")
        self.inpt5 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.inpt5.grid(row=4, column=1, padx=10, pady=10)

        self.lb6 = Label(self.f, text="Select Department", font=font ,bg="#333333", fg="white")
        self.inpt6 = ttk.Combobox(self.f, font=font, width=28, state='readonly', values=self.getDepartments())
        self.lb6.grid(row=6, column=0, padx=10, pady=10)
        self.lb6.grid(row=5, column=0, padx=10, pady=10)
        self.inpt6.grid(row=5, column=1, padx=10, pady=10)

        self.lb7 = Label(self.f, text="Select Category", font=font ,bg="#333333", fg="white")
        self.inpt7 = ttk.Combobox(self.f, font=font, width=28, state='readonly', values=self.getCategories())
        self.lb7.grid(row=6, column=0, padx=10, pady=10)
        self.inpt7.grid(row=6, column=1, padx=10, pady=10)

        self.lb8 = Label(self.f, text="Select Image", font=font ,bg="#333333", fg="white")
        self.inpt8 = Entry(self.f, font=font, width=30, state='readonly', fg="#343638", bg="white")
        self.sltImg = Button(self.f, text="Select", width=10, command=self.selectImage, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.lb8.grid(row=7, column=0, padx=10, pady=10)
        self.inpt8.grid(row=7, column=1, padx=10, pady=10)
        self.sltImg.grid(row=7, column=2, padx=10, pady=10)

        self.lb9 = Label(self.f, text="Enter Password", font=font ,bg="#333333", fg="white")
        self.inpt9 = Entry(self.f, font=font, width=30, show="*", fg="#343638", bg="white")
        self.lb9.grid(row=8, column=0, padx=10, pady=10)
        self.inpt9.grid(row=8, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text='Submit', font=font, command=self.submitForm, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.btn.pack(pady=20)



        self.root.mainloop()


    def selectImage(self):
        emp_name = self.inpt1.get()
        path = askopenfilename(parent= self.root)
        
        img = cv2.imread(path)
        cascade =cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        face = cascade.detectMultiScale(img, 1.1, 4)

        if len(face) == 0:
            msg.showwarning("Failed", "Face not detected!", parent=self.root)
        else:
            img_name = f"{emp_name}_{random.randint(1000, 9999)}.png"
            cv2.imwrite(f"employees_Images/{img_name}", img)
            self.inpt8.configure(state='normal')
            self.inpt8.insert(0, img_name)
            self.inpt8.configure(state='readonly')
            


    def getDepartments(self):
        conn = connect()
        cr = conn.cursor()
        q = f"select name from department"
        cr.execute(q)
        result = cr.fetchall()
        # print(result)
        lst = []
        for i in result:
            lst.append(i[0])
        return lst


    def getCategories(self):
        conn = connect()
        cr = conn.cursor()
        q = f"select name from category"
        cr.execute(q)
        result = cr.fetchall()
        # print(result)
        lst = []
        for i in result:
            lst.append(i[0])
        return lst


    def submitForm(self):
        name = self.inpt1.get()
        fname = self.inpt2.get()
        mobile = self.inpt3.get()
        email = self.inpt4.get()
        address = self.inpt5.get()
        department = self.inpt6.get()
        category = self.inpt7.get()
        image = self.inpt8.get()
        password = self.inpt9.get()


        if len(name)==0 or len(email)==0 or len(mobile)==0 or len(fname)==0 or len(password)==0 or len(address)==0  or len(department)==0 or len(category)==0 or mobile.isalpha():
            msg.showwarning('Warning', 'Please Enter Valid Details.', parent=self.root)
        else:
            if verifyMobile(mobile) == 'Invalid' or verifyEmail(email) == 'Invalid':
                msg.showwarning('Warning',"Invalid Email or Mobile Number", parent=self.root)
            else:
                conn = connect()

                q = f"insert into employee values(null, '{name}', '{fname}', '{mobile}', '{email}', '{address}', '{department}', '{category}', '{image}', '{password}')"

                cr = conn.cursor()
                cr.execute(q)
                conn.commit()

                msg.showinfo("Success", f"{name} has been added as employee", parent=self.root )

                self.inpt1.delete(0, 'end')
                self.inpt2.delete(0, 'end')
                self.inpt3.delete(0, 'end')
                self.inpt4.delete(0, 'end')
                self.inpt5.delete(0, 'end')
                
                self.inpt8.config(state='normal')
                self.inpt8.delete(0, 'end')
                self.inpt8.config(state='readonly')

                self.inpt9.delete(0, 'end')
                self.inpt6.set('')
                self.inpt7.set('')



if __name__ == "__main__":
    Main()