from tkinter import *
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os
from connection import connect
import tkinter.messagebox as msg


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('900x700')

        self.f = Frame(self.root)
        self.f.pack(pady=20)

        self.btn1 = Button(self.f, text="Start", font=('arial', 14), command=self.startVideo)
        self.btn1.grid(row=0, column=0, padx=10, pady=10)

        self.btn2 = Button(self.f, text="stop", font=('arial', 14), command=self.stopVideo)
        self.btn2.grid(row=0, column=1, padx=10, pady=10)


        self.lb = Label(self.root)
        self.lb.pack()



        self.root.mainloop()

    def startVideo(self):
        self.captureBtn = Button(self.root, text="Capture", font=('arial', 14),
                                 command=self.recognizeFace)
        self.captureBtn.pack(pady=20)

        self.video = cv2.VideoCapture(0)
        self.playVideo()


    def playVideo(self):
        flag, self.frame = self.video.read()

        cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        face = cascade.detectMultiScale(self.frame, 1.1, 4)

        for x,y,w,h in face:
            cv2.rectangle(self.frame, (x,y), (x+w, y+h), (255,0,0), 2)
        
        if flag:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = cv2.flip(self.frame, 1)
            img = Image.fromarray(self.frame)

            #here in frame we have image and if we print it we get array of rgb of each pixel but tkinter directly is not able to detect array so we convert it special object that we stored in img variable 

            imgTk = ImageTk.PhotoImage(image=img)
            self.lb.imgTk = imgTk #basically every widget is a dictionary, so we create new key imgTk and set its value imgTk
            self.lb.configure(image=imgTk)
            self.lb.after(20, self.playVideo)

    def stopVideo(self):
        self.video.release()
        cv2.destroyAllWindows()
        self.lb.configure(image="")
        self.captureBtn.destroy()


    def recognizeFace(self):
        image_list = os.listdir('employees_Images')
        # print(image_list)
        for img in image_list:
            try:
                result = DeepFace.verify(img1_path = self.frame, img2_path = f"employees_Images/{img}")
                # print(result)
                if result['verified'] == True:
                    self.fetchEmployee(img)
                    break
                else:
                    print("Face not matched")

            except:
                print('Face not Found')


    def fetchEmployee(self, img):
        self.conn = connect()

        q = f"select id, name, father_name, mobile, email, address, department, category from employee where image='{img}'"

        self.cr = self.conn.cursor()
        self.cr.execute(q)

        data = self.cr.fetchall()

        print(f"data: {data}")
        msg.showinfo("Success", "Attendance Marked")



obj = Main()