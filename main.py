from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import addmessage
import adminlogin, employeelogin, main_Screen
from PIL import Image, ImageTk

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.state('zoomed')
        self.root.config(background="#2B2B2B")

        self.rootMenu = Menu(self.root)
        self.root.configure(menu=self.rootMenu)

        self.rootMenu.add_command(label="Admin", command=lambda: adminlogin.Main())
        self.rootMenu.add_command(label="Employee", command=lambda: employeelogin.Main())
        self.rootMenu.add_command(label="Mark Attendance", command=lambda: main_Screen.Main())
        self.rootMenu.add_command(label="Exit", command=lambda: self.root.destroy())

        # self.mainLabel = Label(self.root, text="Welcome to Attendance Mate", font=('calibri', 28, 'bold'),bg="#2FA572",fg="white", borderwidth=3,relief=RAISED)
        # self.mainLabel.pack(pady=20)

        img = Image.open('mainImg.jpg')
        width=int(self.root.winfo_screenwidth())
        height=int(self.root.winfo_screenheight())
        print(width,height)
        img= img.resize((width,height))
        bg = ImageTk.PhotoImage(img)

        canvas = Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height())
        canvas.pack(fill='both', expand=True)

        canvas.create_image(0, 0, image=bg,anchor='nw')


        self.root.mainloop()




if __name__ == '__main__':
    mainObj = Main()
    # main.root.mainloop()


