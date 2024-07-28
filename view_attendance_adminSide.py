from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import connect
import csv
from tkinter.filedialog import askdirectory


class Main:
    def __init__(self):
        self.root = Toplevel()
        self.root.state("zoomed")
        self.root.config(background="#2B2B2B")

        self.mainlabel = Label(self.root, text='View Attendance', font=('arial',28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainlabel.pack(pady=20)

        self.f = Frame(self.root, padx=10, pady=10)
        self.f.config(bg="#2B2B2B")
        self.f.pack(pady=10)

        self.lb1 = Label(self.f, text="Search Name", font=('arial', 14),bg="#2B2B2B", fg="white")
        self.inpt = Entry(self.f, width=30, font=('arial', 14))
        self.srchbtn = Button(self.f, text="Seach", font=('arial', 14), command=self.searchAttendace , borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.rfshbtn = Button(self.f, text="Reset", font=('arial', 14), command=self.Reset, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff" )
        self.dwnldCSV = Button(self.f, text="Download CSV", font=('arial', 14), command=self.generateCSV, borderwidth=3,relief=GROOVE,activebackground="#2FA572",activeforeground="#fff")
        self.lb1.grid(row=0, column=0, padx=10)
        self.inpt.grid(row=0, column=1, padx=10)
        self.srchbtn.grid(row=0, column=2, padx=10)
        self.rfshbtn.grid(row=0, column=3, padx=10)
        self.dwnldCSV.grid(row=0, column=4, padx=10)


        self.attendanceTable = ttk.Treeview(self.root, columns=('id','emp_id', 'emp_name', 'date', 'time','type'))
        self.attendanceTable.pack(pady=10, padx=20, expand=True, fill='both') 

        self.attendanceTable.heading('id', text='ID')
        self.attendanceTable.heading('emp_id', text='EmpId')
        self.attendanceTable.heading('emp_name', text='Emp Name')
        self.attendanceTable.heading('date', text='Date')
        self.attendanceTable.heading('time', text='Time')
        self.attendanceTable.heading('type', text='Type')

        style = ttk.Style()
        style.configure('Treeview', font=('arial', 14), rowheight=40)
        style.configure('Treeview.Heading', font=('arial', 14))

        self.attendanceTable['show'] = 'headings'
        self.getValues()


        self.root.mainloop()

    def generateCSV(self):
        path = askdirectory(parent=self.root)
        
        with open(f'{path}/Attendance Report Admin.csv', 'w', newline='') as file:
            title = ['Attendance ID', 'Employee ID', 'Employee Name', 'Date', 'Time', 'Type']
            writer = csv.writer(file)
            writer.writerow(title)
            for i in self.attendanceTable.get_children():
                data = self.attendanceTable.item(i)['values']
                writer.writerow(data)
            file.close()
            msg.showinfo('Success', 'File has been Generated')

    def Reset(self):
        self.inpt.delete(0, 'end')
        self.getValues()

    
    def searchAttendace(self):
        text = self.inpt.get()

        q = f"select attendance.id, attendance.emp_id, employee.name, attendance.date, attendance.time, attendance.type from attendance inner join employee on attendance.emp_id=employee.id where employee.name like '%{text}%'"
        
        self.cr.execute(q)
        data = self.cr.fetchall()

        for k in self.attendanceTable.get_children():
            self.attendanceTable.delete(k)
            
        for i in data:
            self.attendanceTable.insert('', index=0, values=i)


    def getValues(self):

        self.conn = connect()

        q = f"select attendance.id, attendance.emp_id, employee.name, attendance.date, attendance.time, attendance.type from attendance inner join employee on attendance.emp_id=employee.id"

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        for k in self.attendanceTable.get_children():
            self.attendanceTable.delete(k) #first it will clear table and then in the next loop it will add values

        for i in data:
            self.attendanceTable.insert('', index=0, values=i)



if __name__ == "__main__":
    Main()