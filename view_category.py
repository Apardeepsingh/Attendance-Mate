from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect


class Main:
    def __init__(self):
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='View Categories', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        self.lb1 = Label(self.f, text="Search Name", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = Entry(self.f, width=30, font=('arial', 14))
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14), command=lambda: self.searchCategory("") , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)
        self.inpt.bind('<Return>', self.searchCategory)


        self.catTable = ttk.Treeview(self.root, columns=('name','description'))
        self.catTable.pack(pady=10, padx=20, expand=True, fill='both') #both means x and y jini v space hgi lele

        self.catTable.heading('name', text='Name')
        self.catTable.heading('description', text='Description')

        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.catTable['show'] = 'headings'
        self.getValues()


        # self.dtlBtn = Button(self.root, text="Delete", font=("arial", 14), width=20, command=self.delCat, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        # self.dtlBtn.pack(pady=20)

        self.root.mainloop()


    def delCat(self):
        if len(self.catTable.selection()) == 0:
            msg.showwarning("Warning", "Please select row!", parent=self.root)
        else:
            res = msg.askokcancel("Delete Admin", "Are you sure you want to delete this admin? ", parent=self.root  )

            if res:
                rowid = self.catTable.selection()[0] #it returns tuple and at 0 we get id of clicked row
                data = self.catTable.item(rowid) #returns dictionary and at values we get our data
                selectedCategory = data['values']
                catName = selectedCategory[0]

                # print(catName)

                q = f"delete from category where name='{catName}'"
                self.cr.execute(q)
                self.conn.commit()

                msg.showinfo("Success", "Admin deleted successfully", parent=self.root )
                self.getValues()



    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()


    def searchCategory(self, event):
        text = self.inpt.get()

        q = f"select name, description from category where name like '%{text}%'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.catTable.get_children():
            self.catTable.delete(k)
            
        for i in data:
            self.catTable.insert('', index=0, values=i)

    def getValues(self):

        self.conn = connect()

        q = f"select name, description from category"

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.catTable.get_children():
            self.catTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.catTable.insert('', index=0, values=i)


if __name__ == "__main__":
    Main()