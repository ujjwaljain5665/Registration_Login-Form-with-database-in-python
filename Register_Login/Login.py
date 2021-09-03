from tkinter import * 
import time
from tkinter import ttk,messagebox
import math
from PIL import Image,ImageTk
from tkinter.constants import TRUE
import pymysql

class login:
    #login window
    def __init__(self,window):
        self.window=window
        self.window.geometry("1280x720-0+0")
        self.window.state('zoomed')
        self.window.config(bg="black")
        self.window.title("Login Window")
        # bg
        leftbg=Label(self.window,bg="#08A3D2",bd=0)
        leftbg.place(x=0,y=0,relheight=1,width=500)
        rightbg=Label(self.window,bg="#031F3C",bd=0)
        rightbg.place(x=500,y=0,relheight=1,relwidth=1)

        #login frame
        loginframe=Frame(self.window,bg="white")
        loginframe.place(x=370,y=70,width=800,height=500)
        # heading
        title=Label(loginframe,text="Login Here",font=("times new roman",30,"bold"),bg="white",fg="#08A3D2").place(x=400,y=10)
        #row-1
        emailid=Label(loginframe,text="Email Address",font=("times new roman",25,"bold"),bg="white",fg="grey").place(x=250,y=90)
        self.text_id=Entry(loginframe,font=("times new roman",15),bg="lightgrey")
        self.text_id.place(x=255,y=140,width=300,height=30)
        #row-2
        password=Label(loginframe,text="Password",font=("times new roman",25,"bold"),bg="white",fg="grey").place(x=250,y=200)
        self.text_pass=Entry(loginframe,font=("times new roman",15),bg="lightgrey")
        self.text_pass.place(x=255,y=250,width=300,height=30)
        # register btn
        btnreg=Button(loginframe,text="New User ? Register Here",command=self.register_window,font=("times new roman",14),cursor="hand2",bd=0,bg="white",fg="#B00857").place(x=255,y=300)
        #forget pass
        btnforpass=Button(loginframe,text="Forgot Password ?",command=self.for_pass,font=("times new roman",14),cursor="hand2",bd=0,bg="white",fg="red").place(x=575,y=300)
        # login butn
        self.logbtn=ImageTk.PhotoImage(file="Images/log.jpg")
        btnlog=Button(loginframe,image=self.logbtn,bg="white",command=self.log_in,bd=0,cursor="hand2").place(x=390,y=370)

        #canvas
        self.canvas = Canvas(self.window, width=365, height=370,bg="black",bd=0,relief='ridge',highlightthickness=0)
        self.canvas.place(x=200,y=140)

        # clocktitle=Label(self.canvas,text="Developer's Clock",font=("times new roman",25,"bold"),bg="white",fg="red").place(x=80,y=4)
        
        # clock image
        self.bg = PhotoImage(file='Images/clock.png')
        self.canvas.create_image(180, 180, image=self.bg)

        #digi clock
        self.clock=Label(self.window,text="00:00:00",font="helvetica 20 bold",bg="black",fg="yellow")
        self.clock.place(x=1110,y=610,width=170,height=50)

        # create clock hands
        self.center_x = 180
        self.center_y = 180

        self.seconds_hand_len = 95
        self.minutes_hand_len = 80
        self.hours_hand_len = 60

        # seconds hand
        self.seconds_hand = self.canvas.create_line(200, 200, 200 + self.seconds_hand_len, 200 + self.seconds_hand_len, width=1.5, fill='red')
        # minutes hand
        self.minutes_hand = self.canvas.create_line(200, 200, 200 + self.minutes_hand_len, 200 + self.minutes_hand_len, width=2, fill='white')
        # hours hand
        self.hours_hand = self.canvas.create_line(200, 200, 200 + self.hours_hand_len, 200 + self.hours_hand_len, width=4, fill='white')

        self.update_clock()
    #login validation
    def log_in(self):
        if self.text_id.get()=="" or self.text_pass.get()=="":
            messagebox.showerror("Error","All Fields are required",parent=self.window)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="register")
                cur=con.cursor()
                cur.execute("select * from login where email=%s and password=%s",(self.text_id.get(),self.text_pass.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Username or Password",parent=self.window)
                else:
                    messagebox.showinfo("Success","Welcome",parent=self.window)
                    self.text_id.delete(0,END)
                    self.text_pass.delete(0,END)
                con.close()
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {e}")
    #clock update
    def update_clock(self):
        self.hours = int(time.strftime("%I"))
        self.minutes = int(time.strftime("%M"))
        self.seconds = int(time.strftime("%S"))

        self.am_or_pm = time.strftime("%p") # for digi
        # updating seconds hand
        self.seconds_x = self.seconds_hand_len * math.sin(math.radians(self.seconds * 6)) + self.center_x
        self.seconds_y = -1 * self.seconds_hand_len * math.cos(math.radians(self.seconds * 6)) + self.center_y
        self.canvas.coords(self.seconds_hand, self.center_x, self.center_y, self.seconds_x, self.seconds_y)

        # updating minutes hand
        self.minutes_x = self.minutes_hand_len * math.sin(math.radians(self.minutes * 6)) + self.center_x
        self.minutes_y = -1 * self.minutes_hand_len * math.cos(math.radians(self.minutes * 6)) + self.center_y
        self.canvas.coords(self.minutes_hand, self.center_x, self.center_y, self.minutes_x, self.minutes_y)

        # updating hours hand
        self.hours_x = self.hours_hand_len * math.sin(math.radians(self.hours * 30 + self.minutes * 0.5)) + self.center_x  #self.hours * 30
        self.hours_y = -1 * self.hours_hand_len * math.cos(math.radians(self.hours * 30 + self.minutes * 0.5)) + self.center_y  #self.hours * 30
        self.canvas.coords(self.hours_hand, self.center_x, self.center_y, self.hours_x, self.hours_y)

        self.time_text = str(self.hours) + ":" + str(self.minutes) + ":" + str(self.seconds) + " " + self.am_or_pm # digi
        self.clock.config(text=self.time_text)

        
        self._job=self.window.after(1000, self.update_clock)
    #passwrd window
    def paa_wind(self):
        self.window2=Toplevel()
        self.window2.title("Reset Password")
        self.window2.geometry("350x400+610+128")
        self.window2.config(bg="white")
        self.window2.focus_force()
        self.window2.grab_set()
        #title
        t=Label(self.window2,text="Forgot Password",font=("times new roman",20,"bold"),bg="white",fg="darkblue").place(x=0,y=10,relwidth=1)
        #sec_ques
        questn=Label(self.window2,text="Security Question",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=100)
        self.cmbquestn=ttk.Combobox(self.window2,font=("times new roman",11),state='readonly',justify=CENTER)
        self.cmbquestn['values']=("Select","Your Pet Name","Your Birth Place","Your Best Friend's Name")
        self.cmbquestn.place(x=50,y=130,width=250)
        self.cmbquestn.current(0)
        #anser
        answer=Label(self.window2,text="Answer",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=170)
        self.tanswer=Entry(self.window2,font=("times new roman",15),bg="lightgrey")
        self.tanswer.place(x=50,y=200,width=250)
        #new pass
        newpassw=Label(self.window2,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=230)
        self.tpassw=Entry(self.window2,font=("times new roman",15),bg="lightgrey")
        self.tpassw.place(x=50,y=260,width=250)
        #button
        btnfornewpass=Button(self.window2,text="Change Password",command=self.chng_pass,font=("times new roman",20,"bold"),cursor="hand2",bd=0,bg="green",fg="white").place(x=60,y=310)
    #chng passwrd
    def chng_pass(self):
        if self.cmbquestn.get()=="Select" or self.tanswer.get()=="" or self.tpassw.get()=="":
            messagebox.showerror("Error","All fields are required",parent=self.window2)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="register")
                cur=con.cursor()
                cur.execute("select * from login where email=%s and question=%s and answer=%s",(self.text_id.get(),self.cmbquestn.get(),self.tanswer.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Enter correct security question / answer to reset your password",parent=self.window2)
                else:
                    cur.execute("update login set password=%s where email=%s",(self.tpassw.get(),self.text_id.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Succeess","Password Changed Successfully",parent=self.window2)
                    self.clear()
                    self.window2.destroy()
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {e}")
    #passwrd window validation
    def for_pass(self):
        if self.text_id.get()=="":
            messagebox.showerror("Error","Please Enter Email to reset your password",parent=self.window)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="register")
                cur=con.cursor()
                cur.execute("select * from login where email=%s",self.text_id.get())
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Enter valid Email to reset your password",parent=self.window)
                else:
                    con.close()
                    self.paa_wind()
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {e}")
    #cancel after method
    def cancel(self):
        if self._job is not None:
            self.window.after_cancel(self._job)
            self._job = None
    #open register window   
    def register_window(self):
        self.cancel()
        self.window.destroy()
        import Register
    #clear
    def clear(self):
        self.cmbquestn.current(0)
        self.tanswer.delete(0,END)
        self.tpassw.delete(0,END)
        self.text_pass.delete(0,END)
        self.text_id.delete(0,END)
        

window = Tk()
ob=login(window)
window.mainloop()