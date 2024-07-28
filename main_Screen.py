import datetime
import tkinter.tix
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import cv2
from deepface import DeepFace
import os
import tkinter.messagebox as msg
from connection import connect
import mailingDemo
# from main import Main as MainClass
# from main import mainObj

class Main:
    def __init__(self):
        # mainObj.root.destroy()

        self.conn = connect()
        self.cr = self.conn.cursor()
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('green')
        windowColor = '#F2BEFC'
        frameColor = '#2b2b2b'
        self.root = customtkinter.CTkToplevel()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        # print(sw, sh)
        self.root.geometry(f"{sw}x{sh}+0+0")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.sideFrame1 = customtkinter.CTkFrame(self.root, height=sh - 100, width=int(sw / 3))
        self.sideFrame1.pack_propagate(0)
        self.sideFrame2 = customtkinter.CTkFrame(self.root, height=sh - 100, width=int(sw / 3 * 2))
        self.sideFrame2.pack_propagate(0)
        self.sideFrame1.grid(row=0, column=0, padx=10, pady=20)
        self.sideFrame2.grid(row=0, column=1, padx=10, pady=20)

        self.mainLabel2 = customtkinter.CTkButton(self.sideFrame1, text='Attendance Mate',font=('arial', 26))
        self.mainLabel2.pack(pady=60)

        self.formFrame = customtkinter.CTkFrame(self.sideFrame1)
        self.formFrame.pack(pady=10, expand=True)
        self.mainLabel1 = customtkinter.CTkButton(self.formFrame, text='Mark Attendance', font=('arial', 20), width=200)
        self.mainLabel1.pack(pady=20)

        # self.lb1 = Label(self.formFrame, text='Enter Vehicle Number', bg=frameColor, font=('arial', 12), fg='white')
        # self.lb1.grid(row=0, column=0)
        self.txt1 = customtkinter.CTkEntry(self.formFrame, placeholder_text='Employee ID :', width=400)
        # self.txt1.grid(row=0, column=1, padx=10)
        self.txt1.pack(pady=10)
        self.txt1.configure(state="readonly")

        # self.btn1 = customtkinter.CTkButton(self.formFrame, text='Search')
        # self.btn1.pack(pady=10)
        self.txt2 = customtkinter.CTkEntry(self.formFrame, placeholder_text='Employee Name', width=400)
        self.txt2.pack(pady=10)
        self.txt2.configure(state="readonly")

        self.txt3 = customtkinter.CTkEntry(self.formFrame, width=400)
        self.txt3.insert(0, datetime.date.today())
        self.txt3.pack(pady=10)
        self.txt3.configure(state="readonly")

        self.txt4 = customtkinter.CTkEntry(self.formFrame, width=400)
        self.txt4.insert(0, str(datetime.datetime.now().time()).split('.')[0])
        self.txt4.pack(pady=10)
        self.txt4.configure(state="readonly")

        self.btn2 = customtkinter.CTkButton(self.formFrame, text='Submit', command=self.markAttendance)
        self.btn2.pack(pady=10)

        self.displayFrame = customtkinter.CTkFrame(self.sideFrame2)
        self.displayFrame.pack(pady=10, expand=True, fill='both', padx=10)

        self.label = customtkinter.CTkLabel(self.displayFrame, text='')
        self.label.pack(anchor=NE)

        self.camLabel = Label(self.displayFrame)
        self.camLabel.pack(anchor=NW)
        # self.cap = cv2.VideoCapture(0)
        # self.show_frames()

        file = Image.open('face.gif')
        self.file_frames = file.n_frames
        self.im = [PhotoImage(file='face.gif', format=f'gif -index {i}') for i in range(self.file_frames)]
        # print(self.im)
        self.frameCount = 0
        self.animnate()

        self.btnFrame = customtkinter.CTkFrame(self.sideFrame2, width=int(sw / 3 * 1.3) + 200)
        self.btnFrame.pack(pady=10, padx=10)
        self.btnFrame.pack_propagate(0)
        self.cameraButton = customtkinter.CTkButton(self.btnFrame, text='Open Camera', command=self.openCamera,font=('arial', 20), width=200)
        self.cameraButton.grid(row=0, column=0, pady=20, padx=10)

        self.themeButton = customtkinter.CTkButton(self.btnFrame, text='Light Theme', font=('arial', 20), width=200,
                                                   command=self.changeTheme)
        self.themeButton.grid(row=0, column=2, pady=20, padx=10)

        self.root.mainloop()

    def openCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.show_frames()
        self.cameraButton.configure(command=self.closeCamera, text='Close Camera')
        self.imageButton = customtkinter.CTkButton(self.btnFrame, text='Capture', font=('arial', 20), width=200,
                                                   command=self.recface)
        self.imageButton.grid(row=0, column=1, pady=20, padx=10)

    def closeCamera(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.camLabel.configure(image='')
        self.cameraButton.configure(command=self.openCamera, text='Open Camera')
        self.imageButton.destroy()


    def markAttendance(self):
        empID = self.txt1.get()
        date = self.txt3.get()
        time = self.txt4.get()
        q = f"select * from attendance where emp_id='{empID}' and date='{date}' and type='out'"
        # print(q)
        self.cr.execute(q)
        data1 = self.cr.fetchone()
        if data1 is None:
            q = f"select * from attendance where emp_id='{empID}' and date='{date}' and type='in'"
            self.cr.execute(q)
            data = self.cr.fetchone()
            if data is None:
                entry = 'in'
            else:
                entry = 'out'
            q = f"insert into attendance values (null, '{empID}', '{date}', '{time}', '{entry}')"
            self.cr.execute(q)
            self.conn.commit()
            self.mailEntry = entry
            msg.showinfo('', f"Entry marked as {entry} on {time}")
            self.sendRemarks()
        else:
            msg.showwarning('Warning',"Attendance has been marked for today..")
        

        self.txt1.configure(state="normal")
        self.txt1.delete(0, 'end')
        self.txt1.configure(state="readonly")

        self.txt2.configure(state="normal")
        self.txt2.delete(0, 'end')
        self.txt2.configure(state="readonly")

        self.txt3.configure(state="normal")
        self.txt3.delete(0, 'end')
        self.txt3.insert(0, datetime.date.today())
        self.txt3.configure(state="readonly")

        self.txt4.configure(state="normal")
        self.txt4.delete(0, 'end')
        self.txt4.insert(0, str(datetime.datetime.now().time()).split('.')[0])
        self.txt4.configure(state="readonly")

        self.root.destroy()



    def recface(self):
        try:
            images = os.listdir('employees_Images')
            for i in images:
                # print(f'images12/{i}')
                result = DeepFace.verify(img1_path=self.frame, img2_path=f'employees_Images/{i}')
                # print(result)
                if result['verified']:
                    # print(i)
                    self.getDetails(i)
                    break
        except ValueError:
            msg.showwarning('Warning', 'Try Again')
    
    def getDetails(self, pic):
    
        q = f"select id, name, father_name, mobile, email, address, department, category from employee where image='{pic}'"

        self.cr.execute(q)
        result = self.cr.fetchone()

        if result is None:
            msg.showwarning('Warning', 'Invalid Data')
        else:
            # print(result)
            self.empName = result[1]
            self.empEmail = result[4]
            
            self.txt1.configure(state="normal")
            self.txt1.delete(0,'end')
            self.txt1.insert(0, result[0])
            self.txt1.configure(state="readonly")

            self.txt2.configure(state="normal")
            self.txt2.delete(0,'end')
            self.txt2.insert(0, result[1])
            self.txt2.configure(state="readonly")


    def sendRemarks(self):
        message = f'''
Dear {self.empName},

I hope this message finds you well. I am writing to let you know that your attendance has been marked for the {self.txt3.get()}/{self.txt4.get()} shift as {self.mailEntry}. 

Thank you for your continued efforts and contribution to the success of our team.'''

        subject = 'Attendance Notification'
        
        mailingDemo.sendEmail(to=self.empEmail, message=message, subject=subject)


    def animnate(self):
        self.label.configure(image=self.im[self.frameCount])
        self.frameCount += 1
        if self.frameCount == self.file_frames:
            self.frameCount = 0

        self.label.after(50, self.animnate)

    def show_frames(self):
        # Get the latest frame and convert into Image
        flag, self.frame = self.cap.read()

        cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        face = cascade.detectMultiScale(self.frame, 1.1, 4) #1.1 scale and 4 average faces in frame

        for x,y,w,h in face:
            cv2.rectangle(self.frame, (x,y), (x+w, y+h), (114,165 , 47), 2)


        if flag:
            self.frame = cv2.resize(self.frame, (920,650))
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = cv2.flip(self.frame, 1)
            img = Image.fromarray(self.frame)
            # Convert image to PhotoImage
            self.frame2 = ImageTk.PhotoImage(image=img)
            self.camLabel.imgtk = self.frame2
            self.camLabel.configure(image=self.frame2)
            # Repeat after an interval to capture continiously
            self.camLabel.after(20, self.show_frames)

    def changeTheme(self):
        if self.themeButton.cget('text') == 'Light Theme':
            customtkinter.set_appearance_mode('light')
            self.themeButton.configure(text='Dark Theme')

        else:
            customtkinter.set_appearance_mode('dark')
            self.themeButton.configure(text='Light Theme')



if __name__ == "__main__":
    Main()
