from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect
from tkcalendar import Calendar, DateEntry
import datetime



class Main():
    def __init__(self, emp_id):
        self.emp_id = emp_id
        # self.root = Tk()
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='Your Leaves', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        self.lb1 = Label(self.f, text="Search Leaves", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = Entry(self.f, width=30, font=('arial', 14))
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14), command=lambda: self.searchMessage(""), borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff" )
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)
        self.inpt.bind('<Return>', self.searchMessage)


        self.leavesTable = ttk.Treeview(self.root, columns=('id','date','remarks', 'status'))
        self.leavesTable.pack(pady=10, padx=20, expand=True, fill='both')

        self.leavesTable.heading('id', text='ID')
        self.leavesTable.heading('date', text='Date')
        self.leavesTable.heading('remarks', text="Remarks")
        self.leavesTable.heading('status', text='Status')

        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.leavesTable['show'] = 'headings'
        self.getValues()
        self.leavesTable.bind("<Double-1>", self.openUpdateWindow)


        self.updtBtn = Button(self.root, text="Update", font=("arial", 14), width=20, command=lambda: self.openUpdateWindow(""), borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.updtBtn.pack(pady=20)


        self.root.mainloop()

    def openUpdateWindow(self, event): #python also sends aditional data with event
        if len(self.leavesTable.selection()) == 0:
            msg.showwarning("Warning", "Please select row!", parent=self.root)
        else:
            rowid = self.leavesTable.selection()[0]
            data = self.leavesTable.item(rowid)
            selectedLeave = data['values']

            self.root1 = Toplevel() #for opening addition window

            self.root1.geometry('900x800')
            self.root1.config(background="#2B2B2B")

            self.mainLabel = Label(self.root1, text="Update Leave", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
            self.mainLabel.pack(pady=20)

            self.f = Frame(self.root1, padx=10, pady=10)
            self.f.config(bg="#333333", borderwidth=3, relief=RIDGE)
            self.f.pack(pady=10)

            font = ('calibri', 14)

            self.lb0 = Label(self.f, text='Leave ID', font=font,bg="#333333", fg="white")
            self.txt0 = Entry(self.f, font=font, width=30)
            self.lb0.grid(row=0, column=0, pady=10, padx=10)
            self.txt0.grid(row=0, column=1, pady=10, padx=10)
            self.txt0.insert(0, selectedLeave[0]) #0 is starting index of string
            self.txt0.config(state='readonly')


            if selectedLeave[3] == "Pending":
                self.lb1 = Label(self.f, text="Select Date", font=font,bg="#333333", fg="white")
                self.txt1 = DateEntry(self.f, font=font, width=28, state="readonly", date_pattern='yyyy-MM-dd')
                self.lb1.grid(row=1, column=0, pady=10, padx=10)
                self.txt1.grid(row=1, column=1, pady=10, padx=10)
                self.txt1.insert(0, selectedLeave[1])

                self.lb2 = Label(self.f, text="Enter Remarks", font=font,bg="#333333", fg="white")
                self.txt2 = Entry(self.f, font=font, width=30)
                self.lb2.grid(row=2, column=0, pady=10, padx=10)
                self.txt2.grid(row=2, column=1, pady=10, padx=10)
                self.txt2.insert(0, selectedLeave[2])

                self.lb3 = Label(self.f, text='Change Status', font=font,bg="#333333", fg="white")
                self.txt3 = ttk.Combobox(self.f, font=font, width=28, values="Withdraw")
                self.lb3.grid(row=3, column=0, pady=10, padx=10)
                self.txt3.grid(row=3, column=1, pady=10, padx=10)
                self.txt3.insert(0, selectedLeave[3])
                self.txt3.config(state='readonly')
            else:
                self.lbs0 = Label(self.f, text='*Date Cannot be Changed', font=('calibri', 10), fg='#BB2D3B',bg="#333333")
                self.lb1 = Label(self.f, text="Select Date", font=font,bg="#333333", fg="white")
                self.txt1 = Entry(self.f, font=font, width=30)
                self.lb1.grid(row=1, column=0, pady=10, padx=10)
                self.txt1.grid(row=1, column=1, pady=10, padx=10)
                self.lbs0.grid(row=1, column=2, pady=10, padx=10)
                self.txt1.insert(0, selectedLeave[1])
                self.txt1.config(state="readonly")

                self.lbs1 = Label(self.f, text='*Remarks Cannot be Changed', font=('calibri', 10), fg='#BB2D3B',bg="#333333")
                self.lb2 = Label(self.f, text="Enter Remarks", font=font,bg="#333333", fg="white")
                self.txt2 = Entry(self.f, font=font, width=30)
                self.lb2.grid(row=2, column=0, pady=10, padx=10)
                self.txt2.grid(row=2, column=1, pady=10, padx=10)
                self.lbs1.grid(row=2, column=2, pady=10, padx=10)
                self.txt2.insert(0, selectedLeave[2])
                self.txt2.config(state="readonly")

                self.lbs2 = Label(self.f, text='*Status Cannot be Changed', font=('calibri', 10), fg='#BB2D3B',bg="#333333")
                self.lb3 = Label(self.f, text='Change Status', font=font,bg="#333333", fg="white")
                self.txt3 = Entry(self.f, font=font, width=30)
                self.lb3.grid(row=3, column=0, pady=10, padx=10)
                self.txt3.grid(row=3, column=1, pady=10, padx=10)
                self.lbs2.grid(row=3, column=2, pady=10, padx=10)
                self.txt3.insert(0, selectedLeave[3])
                self.txt3.config(state='readonly')


            self.btn = Button(self.root1, text='Submit', font=font, command=self.updateLeave, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
            self.btn.pack(pady=20)
            

            self.root1.mainloop()


    def updateLeave(self):
        id = self.txt0.get()
        date = self.txt1.get()
        remarks = self.txt2.get()
        status = self.txt3.get()

        q = f"update leaves set date='{date}',  remarks='{remarks}', status='{status}' where id = '{id}' "

        self.cr.execute(q)
        self.conn.commit()

        msg.showinfo("Success", "Leave has been updated", parent=self.root1)
        self.getValues()
        self.root1.destroy()


    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()

    
    def searchMessage(self, event):
        text = self.inpt.get()

        q = f"select id, date, remarks, status from leaves where emp_id={self.emp_id} and remarks like '%{text}%'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.leavesTable.get_children():
            self.leavesTable.delete(k)
            
        for i in data:
            self.leavesTable.insert('', index=0, values=i)
            

    def getValues(self):
        self.conn = connect()

        q = f"select id, date, remarks, status from leaves where emp_id={self.emp_id}"

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.leavesTable.get_children():
            self.leavesTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.leavesTable.insert('', index=0, values=i)



if __name__ == "__main__":
    Main(5)