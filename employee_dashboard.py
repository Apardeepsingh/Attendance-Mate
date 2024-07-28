from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import addleave, view_leaves_employeeSide
import addmessage
import view_attendance_employeeSide, main_Screen, changePassword_emp


class Main:
    def __init__(self, emp_id):
        self.emp_id = emp_id
        self.root = Tk()
        self.root.state('zoomed')
        self.root.config(background="#2B2B2B")

        self.rootMenu = Menu(self.root)
        self.root.configure(menu=self.rootMenu)

        self.profileSubMenu = Menu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Profile', menu=self.profileSubMenu)
        self.profileSubMenu.add_command(label="Change Password", command=lambda: changePassword_emp.Main(emp_id) )
        self.profileSubMenu.add_command(label="Logout", command=lambda: self.root.destroy())

        self.leaveSubMenu = Menu( self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Manage Leaves', menu=self.leaveSubMenu)
        self.leaveSubMenu.add_command( label="Request Leave", command=lambda: addleave.Main(emp_id))
        self.leaveSubMenu.add_command( label="View Leaves", command=lambda: view_leaves_employeeSide.Main(emp_id))

        self.attendanceSubMenu = Menu( self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Manage Attendance', menu=self.attendanceSubMenu)
        # self.attendanceSubMenu.add_command( label="Mark Attendance", command=lambda: main_Screen.Main())
        self.attendanceSubMenu.add_command( label="View Attendance", command=lambda: view_attendance_employeeSide.Main(emp_id))


        self.rootMenu.add_command(label="Messages", command=lambda: addmessage.Main(emp_id))

        self.mainLabel = Label(self.root, text="Welcome to Employee Dashboard", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)

        self.root.mainloop()


if __name__ == "__main__":
    Main(9)