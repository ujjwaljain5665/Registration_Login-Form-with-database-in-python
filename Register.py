from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql

'''
we can fetch data in 2 ways:
    1.self.fnameval=StringVar()
    fname=Label(frame1,text="First Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=50)
    tfname=Entry(frame1,font=("times new roman",15),bg="lightgrey",textvariable=self.fnameval).place(x=50,y=80,width=250)
    
    2.lname=Label(frame1,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=400,y=50)
    self.tlname=Entry(frame1,font=("times new roman",15),bg="lightgrey")
    self.tlname.place(x=400,y=80,width=250)
'''

class register:
    # register window
    def __init__(self,root):
        self.root=root
        self.root.title("Registration Form")
        self.root.geometry("1280x720-0+0")
        self.root.config(bg="white")

        # BG
        self.bg=ImageTk.PhotoImage(file="Images/bg3.jpeg")
        bg=Label(self.root,image=self.bg).place(x=250,y=0,relheight=1,relwidth=1)

        # Front left image
        self.left=ImageTk.PhotoImage(file="Images/bg7.jpg")
        bg=Label(self.root,image=self.left,bg="black").place(x=100,y=110,height=450,width=350)

        # Frame
        frame1=Frame(self.root,bg="white")
        frame1.place(x=450,y=110,width=700,height=450)

        # Heading
        title=Label(frame1,text="Registration Form",font=("times new roman",20,"bold"),bg="white",fg="red").place(x=230,y=6)

        # Row 1
        fname=Label(frame1,text="First Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=50)
        self.tfname=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.tfname.place(x=50,y=80,width=250)

        lname=Label(frame1,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=400,y=50)
        self.tlname=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.tlname.place(x=400,y=80,width=250)

        # Row 2
        cont=Label(frame1,text="Contact",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=120)
        self.tcont=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.tcont.place(x=50,y=150,width=250)

        email=Label(frame1,text="Email Id",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=400,y=120)
        self.temail=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.temail.place(x=400,y=150,width=250)

        # Row 3
        questn=Label(frame1,text="Security Question",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=190)

        self.cmbquestn=ttk.Combobox(frame1,font=("times new roman",11),state='readonly',justify=CENTER)
        self.cmbquestn['values']=("Select","Your Pet Name","Your Birth Place","Your Best Friend's Name")
        self.cmbquestn.place(x=50,y=220,width=250)
        self.cmbquestn.current(0)

        answer=Label(frame1,text="Answer",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=400,y=190)
        self.tanswer=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.tanswer.place(x=400,y=220,width=250)

        # Row 4
        passw=Label(frame1,text="Password",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=50,y=260)
        self.tpassw=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.tpassw.place(x=50,y=290,width=250)

        confpass=Label(frame1,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=400,y=260)
        self.tconfpass=Entry(frame1,font=("times new roman",15),bg="lightgrey")
        self.tconfpass.place(x=400,y=290,width=250)

        # Terms
        self.chkbtnval=IntVar()
        chkbtn=Checkbutton(frame1,text="I Agree The Terms And Conditions",variable=self.chkbtnval,onvalue=1,offvalue=0,bg="white",font=("times new roman",12)).place(x=50,y=330)

        # Register Button
        self.btn=ImageTk.PhotoImage(file="Images/bg6.jpg")
        btnreg=Button(frame1,image=self.btn,bd=0,cursor="hand2",command=self.data).place(x=220,y=380)

        # Sign in Button
        btnlog=Button(self.root,text="Sign In",command=self.login_window,font=("times new roman",20),bd=0,cursor="hand2").place(x=190,y=465,width=150)
    #clear fields
    def clear(self):
        self.tfname.delete(0,END)
        self.tlname.delete(0,END)
        self.tcont.delete(0,END)
        self.temail.delete(0,END)
        self.tpassw.delete(0,END)
        self.tconfpass.delete(0,END)
        self.tanswer.delete(0,END)
        self.cmbquestn.current(0)
        self.chkbtnval=0
    #data fetch and validation
    def data(self):

        # validation 
        if self.tfname.get()=="" or self.tlname.get()=="" or self.tcont.get()=="" or self.temail.get()=="" or self.cmbquestn.get()=="" or self.tanswer.get()=="" or self.tpassw.get()=="" or self.tconfpass.get()=="":
            messagebox.showerror("Error","All Fields Are Compulsary",parent=self.root)
        elif self.tpassw.get()!=self.tconfpass.get():
            messagebox.showerror("Error","Password and Confirm Password doesn't match",parent=self.root)
        elif self.chkbtnval.get() != 1:
            messagebox.showerror("Error","Please Agree to our Terms and Conditions",parent=self.root)
        else:
            try:
                con=pymysql.connect(host="localhost",user="root",password="",database="register")
                cur=con.cursor()
                cur.execute("select * from login where email=%s",self.temail.get())
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","User already exist.Please try another email.",parent=self.root)
                else:
                    cur.execute("insert into login (FIRST_NAME,LAST_NAME,CONTACT,EMAIL,QUESTION,ANSWER,PASSWORD) values (%s,%s,%s,%s,%s,%s,%s)",(self.tfname.get(),self.tlname.get(),self.tcont.get(),self.temail.get(),self.cmbquestn.get(),self.tanswer.get(),self.tpassw.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Registration Successful",parent=self.root)
                    self.clear()
            except Exception as e:
                messagebox.showerror("Error",f"Error due to {str(e)}",parent=self.root)
    #open login window
    def login_window(self):
        self.root.destroy()
        import Login
            

root=Tk()
obj=register(root)
root.mainloop()