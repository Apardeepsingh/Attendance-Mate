from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import addadmin, view_admin
import adddepartment, view_department
import addcategory, view_category
import addemployee, view_employee
import view_attendance_adminSide, view_leaves_adminSide, view_messages, changePassword_admin


class Main:
    def __init__(self, admin_id):
        self.root = Tk()
        self.root.state('zoomed')
        self.root.config(background="#2B2B2B")

        self.rootMenu = Menu(self.root)
        self.root.configure(menu=self.rootMenu)
        
        self.profileSubMenu = Menu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Profile', menu=self.profileSubMenu)
        self.profileSubMenu.add_command(label="Change Password", command=lambda: changePassword_admin.Main(admin_id))
        self.profileSubMenu.add_command(label="Logout", command=lambda: self.root.destroy())

        self.adminSubMenu = Menu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Manage Admins', menu=self.adminSubMenu)
        self.adminSubMenu.add_command(label="Add Admin", command=lambda: addadmin.Main())
        self.adminSubMenu.add_command(label="View Admins", command=lambda: view_admin.Main())

        self.categorySubMenu = Menu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Manage Category', menu=self.categorySubMenu)
        self.categorySubMenu.add_command(label="Add Category", command=lambda: addcategory.Main())
        self.categorySubMenu.add_command(label="View Categories", command=lambda: view_category.Main())

        self.departmentSubMenu = Menu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Manage Departments', menu=self.departmentSubMenu)
        self.departmentSubMenu.add_command(label="Add Department", command=lambda: adddepartment.Main())
        self.departmentSubMenu.add_command(label="View Departments", command=lambda: view_department.Main())

        self.employeeSubMenu = Menu(self.rootMenu, tearoff=0)
        self.rootMenu.add_cascade(label='Manage Employees', menu=self.employeeSubMenu)
        self.employeeSubMenu.add_command(label="Add Employee", command=lambda: addemployee.Main())
        self.employeeSubMenu.add_command(label="View Employees", command=lambda: view_employee.Main())

        self.rootMenu.add_command(label="Attendance", command=lambda: view_attendance_adminSide.Main())

        self.rootMenu.add_command(label="Leaves", command=lambda: view_leaves_adminSide.Main())

        self.rootMenu.add_command(label="Messages", command=lambda: view_messages.Main())


        self.mainLabel = Label(self.root, text="Welcome to Admin Dashboard", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        self.mainLabel.pack(pady=20)


        self.root.mainloop()




if __name__ == "__main__":
    Main()