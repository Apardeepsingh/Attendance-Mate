from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect, verifyMobile, verifyEmail


class Main:
    def __init__(self):
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='View Admins', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        self.lb1 = Label(self.f, text="Search Name", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = Entry(self.f, width=30, font=('arial', 14))
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14),  command=lambda: self.searchAdmin("") , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)
        self.inpt.bind('<Return>', self.searchAdmin)


        self.adminTable = ttk.Treeview(self.root, columns=('id','name','email', 'mobile','role'))
        self.adminTable.pack(pady=10, padx=20, expand=True, fill='both') #both means x and y jini v space hgi lele

        self.adminTable.heading('id', text='ID')
        self.adminTable.heading('name', text='Name')
        self.adminTable.heading('email', text='Email')
        self.adminTable.heading('mobile', text='Mobile')
        self.adminTable.heading('role', text='Role')
        # self.adminTable.configure(bg="#333333", borderwidth=3, relief=RIDGE)
        
        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.adminTable['show'] = 'headings'
        self.getValues()
        self.adminTable.bind("<Double-1>", self.openUpdateWindow) #this is event: bind will add the event to each row of table and Double is mouse event and 1 is id for left click 

        self.f2 = Frame(self.root, padx=10, pady=10)
        self.f2.config(bg="#2B2B2B")
        self.f2.pack(pady=20)

        self.dtlBtn = Button(self.f2, text="Delete", font=("arial", 14), width=20, command=self.delAdmin, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.dtlBtn.grid(row=0, column=0, padx=10)

        self.updtBtn = Button(self.f2, text="Update", font=("arial", 14), width=20, command=lambda: self.openUpdateWindow(""), borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.updtBtn.grid(row=0, column=1, padx=10)


        self.root.mainloop()

    def openUpdateWindow(self, event): #python also sends aditional data with event
        if len(self.adminTable.selection()) == 0:
            msg.showwarning("Warning", "Please select row!", parent=self.root)
        else:
            rowid = self.adminTable.selection()[0]
            data = self.adminTable.item(rowid)
            selectedAdmin = data['values']

            self.root1 = Toplevel() #for opening addition window

            self.root1.geometry('900x800')
            self.root1.config(background="#2B2B2B")

            self.mainLabel = Label(self.root1, text="Update Admin", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
            self.mainLabel.pack(pady=20)

            self.f = Frame(self.root1, padx=10, pady=10)
            self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
            self.f.pack(pady=10)

            font = ('calibri', 14)

            self.lb0 = Label(self.f, text='Admin ID', font=font, bg="#333333", fg="white")
            self.txt0 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb0.grid(row=0, column=0, pady=10, padx=10)
            self.txt0.grid(row=0, column=1, pady=10, padx=10)
            self.txt0.insert(0, selectedAdmin[0]) #0 is starting index of string
            self.txt0.config(state='readonly')

            self.lb1 = Label(self.f, text='Enter Name', font=font, bg="#333333", fg="white")
            self.txt1 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb1.grid(row=1, column=0, pady=10, padx=10)
            self.txt1.grid(row=1, column=1, pady=10, padx=10)
            self.txt1.insert(0, selectedAdmin[1])

            self.lb2 = Label(self.f, text='Enter Email', font=font, bg="#333333", fg="white")
            self.txt2 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb2.grid(row=2, column=0, pady=10, padx=10)
            self.txt2.grid(row=2, column=1, pady=10, padx=10)
            self.txt2.insert(0, selectedAdmin[2])
            
            self.lb3 = Label(self.f, text='Enter Mobile', font=font, bg="#333333", fg="white")
            self.txt3 = Entry(self.f, font=font, width=30, fg="#343638", bg="white")
            self.lb3.grid(row=3, column=0, pady=10, padx=10)
            self.txt3.grid(row=3, column=1, pady=10, padx=10)
            self.txt3.insert(0, selectedAdmin[3])

            self.lb4 = Label(self.f, text='Select Role', font=font, bg="#333333", fg="white")
            self.txt4 = ttk.Combobox(self.f, font=font, width=28, state='readonly', values=['Super Admin', 'Admin'])
            self.lb4.grid(row=4, column=0, pady=10, padx=10)
            self.txt4.grid(row=4, column=1, pady=10, padx=10)
            self.txt4.set(selectedAdmin[4])

            self.btn = Button(self.root1, text='Submit', font=font, command=self.updateAdmin, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
            self.btn.pack(pady=20)

            self.root1.mainloop()

    def updateAdmin(self):
        id = self.txt0.get()
        name = self.txt1.get()
        email = self.txt2.get()
        mobile = self.txt3.get()
        role = self.txt4.get()

        if verifyMobile(mobile) == 'Invalid' or verifyEmail(email) == 'Invalid':
            msg.showwarning('Warning',"Invalid Email or Mobile Number", parent=self.root1)
        else:

            q = f"update admin set name='{name}', email='{email}', mobile='{mobile}', role='{role}' where id = '{id}' "

            self.cr.execute(q)
            self.conn.commit()

            msg.showinfo("Success", "Admin has been updated", parent=self.root)
            self.getValues()
            self.root1.destroy()

    def delAdmin(self):
        if len(self.adminTable.selection()) == 0:
            msg.showwarning("Warning", "Please select row!", parent=self.root)
        else:
            res = msg.askokcancel("Delete Admin", "Are you sure you want to delete this admin? ", parent=self.root  )

            if res:
                rowid = self.adminTable.selection()[0] #it returns tuple and at 0 we get id of clicked row
                data = self.adminTable.item(rowid) #returns dictionary and at values we get our data
                selectedAdmin = data['values']
                adminId = selectedAdmin[0]

                q = f"delete from admin where id={adminId}"
                self.cr.execute(q)
                self.conn.commit()

                msg.showinfo("Success", "Admin deleted successfully", parent=self.root )
                self.getValues()


    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()

    
    def searchAdmin(self, event):
        text = self.inpt.get()

        q = f"select id, name, email, mobile, role from admin where name like '%{text}%'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.adminTable.get_children():
            self.adminTable.delete(k)
            
        for i in data:
            self.adminTable.insert('', index=0, values=i)



    def getValues(self):

        self.conn = connect()

        q = f"select id, name, email, mobile, role from admin"

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.adminTable.get_children():
            self.adminTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.adminTable.insert('', index=0, values=i)




if __name__ == "__main__":
    Main()