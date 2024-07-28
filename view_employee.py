from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect, verifyMobile, verifyEmail
import csv
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import cv2, random
import os


class Main:
    def __init__(self):
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='View Employees', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        self.lb1 = Label(self.f, text="Search Name", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = Entry(self.f, width=30, font=('arial', 14))
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14), command=lambda: self.searchEmployee("") , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.dwnldCSV = Button(self.f, text="Download CSV", font=('arial', 14), command=self.generateCSV, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)
        self.dwnldCSV.grid(row=0, column=4, padx=10)
        self.inpt.bind('<Return>', self.searchEmployee)

        self.employeeTable = ttk.Treeview(self.root, columns=('id','name','father_name', 'mobile','email', 'address','department','category','image'))
        self.employeeTable.pack(pady=10, padx=20, expand=True, fill='both') #both means x and y jini v space hgi lele

        self.employeeTable.heading('id', text='ID')
        self.employeeTable.heading('name', text='Name')
        self.employeeTable.heading('father_name', text="Father's Name")
        self.employeeTable.heading('mobile', text='Mobile')
        self.employeeTable.heading('email', text='Email')
        self.employeeTable.heading('address', text='Address')
        self.employeeTable.heading('department', text='Department')
        self.employeeTable.heading('category', text='Category')
        self.employeeTable.heading('image', text='Image')

        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.employeeTable['show'] = 'headings'
        self.getValues()
        self.employeeTable.bind("<Double-1>", self.openUpdateWindow) 

        self.f2 = Frame(self.root, padx=10, pady=10)
        self.f2.config(bg="#2B2B2B")
        self.f2.pack(pady=20)

        # self.dtlBtn = Button(self.f2, text="Delete", font=("arial", 14), width=20, command=self.delEmployee, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        # self.dtlBtn.grid(row=0, column=0, padx=10)

        self.updtBtn = Button(self.f2, text="Update", font=("arial", 14), width=20, command=lambda: self.openUpdateWindow(""), borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.updtBtn.grid(row=0, column=1, padx=10)


        self.root.mainloop()


    def openUpdateWindow(self, event): #python also sends aditional data with event
        if len(self.employeeTable.selection()) == 0:
            msg.showwarning("Warning", "Please select row!", parent=self.root)
        else:
            rowid = self.employeeTable.selection()[0]
            data = self.employeeTable.item(rowid)
            selectedEmployee = data['values']

            global oldImg
            oldImg = selectedEmployee[8]

            self.root1 = Toplevel() #for opening addition window

            self.root1.geometry('900x800')
            self.root1.config(background="#2B2B2B")

            self.mainLabel = Label(self.root1, text="Update Employee", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
            self.mainLabel.pack(pady=20)

            self.f = Frame(self.root1, padx=10, pady=10)
            self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
            self.f.pack(pady=10)

            font = ('calibri', 14)

            self.lb0 = Label(self.f, text='Employee ID', font=font,bg="#333333", fg="white")
            self.txt0 = Entry(self.f, font=font, width=30)
            self.lb0.grid(row=0, column=0, pady=10, padx=10)
            self.txt0.grid(row=0, column=1, pady=10, padx=10)
            self.txt0.insert(0, selectedEmployee[0]) #0 is starting index of string
            self.txt0.config(state='readonly')

            self.lb1 = Label(self.f, text='Enter Name', font=font,bg="#333333", fg="white")
            self.txt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb1.grid(row=1, column=0, pady=10, padx=10)
            self.txt1.grid(row=1, column=1, pady=10, padx=10)
            self.txt1.insert(0, selectedEmployee[1])

            self.lb2 = Label(self.f, text="Enter Father's Name", font=font,bg="#333333", fg="white")
            self.txt2 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb2.grid(row=2, column=0, pady=10, padx=10)
            self.txt2.grid(row=2, column=1, pady=10, padx=10)
            self.txt2.insert(0, selectedEmployee[2])

            self.lb3 = Label(self.f, text='Enter Mobile', font=font,bg="#333333", fg="white")
            self.txt3 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb3.grid(row=3, column=0, pady=10, padx=10)
            self.txt3.grid(row=3, column=1, pady=10, padx=10)
            self.txt3.insert(0, selectedEmployee[3])

            self.lb4 = Label(self.f, text='Enter Email', font=font,bg="#333333", fg="white")
            self.txt4 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb4.grid(row=4, column=0, pady=10, padx=10)
            self.txt4.grid(row=4, column=1, pady=10, padx=10)
            self.txt4.insert(0, selectedEmployee[4])

            self.lb5 = Label(self.f, text='Enter Address', font=font,bg="#333333", fg="white")
            self.txt5 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb5.grid(row=5, column=0, pady=10, padx=10)
            self.txt5.grid(row=5, column=1, pady=10, padx=10)
            self.txt5.insert(0, selectedEmployee[5])

            self.lb6 = Label(self.f, text='Select Department', font=font,bg="#333333", fg="white")
            self.txt6 = ttk.Combobox(self.f, font=font, width=28, state='readonly', values=self.getDepartments())
            self.lb6.grid(row=6, column=0, pady=10, padx=10)
            self.txt6.grid(row=6, column=1, pady=10, padx=10)
            self.txt6.set(selectedEmployee[6])

            self.lb7 = Label(self.f, text='Select Category', font=font,bg="#333333", fg="white")
            self.txt7 = ttk.Combobox(self.f, font=font, width=28, state='readonly', values=self.getCategories())
            self.lb7.grid(row=7, column=0, pady=10, padx=10)
            self.txt7.grid(row=7, column=1, pady=10, padx=10)
            self.txt7.set(selectedEmployee[7])

            self.lb8 = Label(self.f, text='Select Image', font=font,bg="#333333", fg="white")
            self.txt8 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")       
            self.sltImg = Button(self.f, text="Select", width=10, command=self.selectImage, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
            self.lb8.grid(row=8, column=0, pady=10, padx=10)
            self.txt8.grid(row=8, column=1, pady=10, padx=10)
            self.sltImg.grid(row=8, column=2, padx=10, pady=10)
            self.txt8.insert(0, selectedEmployee[8])
            self.txt8.config(state='readonly')

            self.btn = Button(self.root1, text='Submit', font=font, command=self.updateEmployee, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
            self.btn.pack(pady=20)
            

            self.root1.mainloop()


    def selectImage(self):
        emp_name = self.txt1.get()
        oldImageName = self.txt8.get()
        path = askopenfilename(parent= self.f)
        
        img = cv2.imread(path)
        cascade =cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        face = cascade.detectMultiScale(img, 1.1, 4)

        if len(face) == 0:
            msg.showwarning("Failed", "Face not detected!", parent=self.root)
        else:
            img_name = f"{emp_name}_{random.randint(1000, 9999)}.png"
            os.remove(f"employees_Images/{oldImageName}")
            cv2.imwrite(f"employees_Images/{img_name}", img)
            
            self.txt8.configure(state='normal')
            self.txt8.delete(0, END)
            self.txt8.insert(0, img_name)
            self.txt8.configure(state='readonly')


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


    def generateCSV(self):
        path = askdirectory(parent=self.root)
        
        if len(path) != 0:
            with open(f'{path}/Attendance Report Admin.csv', 'w', newline='') as file:
                title = ['Attendance ID', 'Employee ID', 'Employee Name', 'Date', 'Time', 'Type']
                writer = csv.writer(file)
                writer.writerow(title)
                for i in self.attendanceTable.get_children():
                    data = self.attendanceTable.item(i)['values']
                    writer.writerow(data)
                file.close()
                msg.showinfo('Success', 'File has been Generated')

            
    def updateEmployee(self):
        
        id = self.txt0.get()
        name = self.txt1.get()
        fname = self.txt2.get()
        mobile = self.txt3.get()
        email = self.txt4.get()
        address = self.txt5.get()
        department = self.txt6.get()
        category = self.txt7.get()
        image = self.txt8.get()

        if verifyMobile(mobile) == 'Invalid' or verifyEmail(email) == 'Invalid':
                msg.showwarning('Warning',"Invalid Email or Mobile Number", parent=self.root1)
        else:
            # img = cv2.imread(f"employees_Images/{image}")
            if image==oldImg:
                img_name = f"{name}_{random.randint(1000, 9999)}.png"
                os.rename(f"employees_Images/{image}" ,f"employees_Images/{img_name}")

                self.txt8.configure(state='normal')
                self.txt8.delete(0, END)
                self.txt8.insert(0, img_name)
                self.txt8.configure(state='readonly')

                q = f"update employee set name='{name}',  father_name='{fname}', mobile='{mobile}',email='{email}', address='{address}', department='{department}', category='{category}', image='{img_name}' where id = '{id}' "
            else:
                q = f"update employee set name='{name}',  father_name='{fname}', mobile='{mobile}',email='{email}', address='{address}', department='{department}', category='{category}', image='{image}' where id = '{id}' "


            self.cr.execute(q)
            self.conn.commit()

            msg.showinfo("Success", "Employee has been updated", parent=self.root1)
            self.getValues()
            self.root1.destroy()


    def delEmployee(self):
        if len(self.employeeTable.selection()) == 0:
            msg.showwarning("Warning", "Please select row!", parent=self.root)
        else:
            res = msg.askokcancel("Delete Employee", "Are you sure? ", parent=self.root  )

            if res:
                rowid = self.employeeTable.selection()[0] #it returns tuple and at 0 we get id of clicked row
                data = self.employeeTable.item(rowid) #returns dictionary and at values we get our data
                selectedEmployee = data['values']
                employeeId = selectedEmployee[0]

                q = f"delete from employee where id={employeeId}"
                self.cr.execute(q)
                self.conn.commit()

                msg.showinfo("Success", "Employee deleted successfully", parent=self.root )
                self.getValues()


    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()

    
    def searchEmployee(self, event):
        text = self.inpt.get()

        q = f"select id, name, father_name, mobile, email, address, department,category, image from employee where name like '%{text}%'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.employeeTable.get_children():
            self.employeeTable.delete(k)
            
        for i in data:
            self.employeeTable.insert('', index=0, values=i)


    def getValues(self):

        self.conn = connect()

        q = f"select id, name, father_name, mobile, email, address, department,category, image from employee "

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.employeeTable.get_children():
            self.employeeTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.employeeTable.insert('', index=0, values=i)



if __name__ == "__main__":
    Main()