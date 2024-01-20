from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import  ImageTk

from tkinter import messagebox


class LoginFrame(tk.Frame):
    def __init__(self, root, client_socket, switch_to_signup_callback, switch_to_dashboard_callback):
        super().__init__(root)
        self.root = root
        self.root.title("GPT4UP")
        self.root.config(bg="white")
        self.client_socket = client_socket
        self.switch_to_signup_callback = switch_to_signup_callback
        self.switch_to_dashboard_callback = switch_to_dashboard_callback
        self.create_widgets()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        msg = f"#{username},{password}"
        self.client_socket.send(msg.encode('utf-8'))
        self.reset_fields()
        
        self.switch_to_dashboard_callback()



    def switch_to_signup(self):
        self.switch_to_signup_callback()

    def reset_fields(self):
        self.entry_username.delete(0, END)
        self.entry_password.delete(0,END)


    def forgot_func(self):
        if self.entry_username.get()=="":
            messagebox.showerror("Error!", "Please enter your Email Id",parent=self.root)
        else:
            try:
               
                username=self.entry_username.get()
                msg = f"-{username}"
                self.client_socket.send(msg.encode('utf-8'))
                self.verification()

            except Exception as er:
                        messagebox.showerror("Error!", f"{er}")
      

    def verification(self):
         
         recv_msg = self.client_socket.recv(1024).decode('utf-8')
         if recv_msg == None:
            messagebox.showerror("Error!", "Email Id doesn't exists")

         else:

                    self.root=Toplevel()
                    self.root.title("Forget Password?")
                    self.root.geometry("400x440+450+200")
                    self.root.config(bg="white")
                    self.root.focus_force()
                    self.root.grab_set()

                    title3 = Label(self.root,text="Change your password",font=("times new roman",20,"bold"),bg="white").place(x=10,y=10)

                    title4 = Label(self.root,text="It's quick and easy",font=("times new roman",12),bg="white").place(x=10,y=45)

                    title5 = Label(self.root, text="Select your question", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=85)

                    self.sec_ques = ttk.Combobox(self.root,font=("times new roman",13),state='readonly',justify=CENTER)
                    self.sec_ques['values'] = ("Select","What's your pet name?","Your first teacher name","Your birthplace", "Your favorite movie")
                    self.sec_ques.place(x=10,y=120, width=270)
                    self.sec_ques.current(0)
                    
                    title6 = Label(self.root, text="Answer", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=160)

                    self.ans = Entry(self.root,font=("arial"))
                    self.ans.place(x=10,y=195,width=270)

                    title7 = Label(self.root, text="New Password", font=("times new roman", 15, "bold"), bg="white").place(x=10,y=235)

                    self.new_pass = Entry(self.root,font=("arial"))
                    self.new_pass.place(x=10,y=270,width=270)

                    self.create_button = Button(self.root,text="Submit",command=self.change_pass,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="green2",fg="white").place(x=95,y=340,width=200)
                
                

    def change_pass(self):
        if self.entry_username.get() == "" or self.sec_ques.get() == "Select" or self.new_pass.get() == "":
            messagebox.showerror("Error!", "Please fill the all entry field correctly")
        else:
            try:
                email=self.entry_username.get()
                question=self.sec_ques.get()
                answer=self.ans.get()
                msg = f"*{email},{question},{answer}"
                self.client_socket.send(msg.encode('utf-8'))

                self.change()      
            except Exception as er:
                        messagebox.showerror("Error!", f"{er}")

    def change(self):
                
                msg = self.client_socket.recv(1024).decode('utf-8')
                
                if msg == None:
                    messagebox.showerror("Error!", "Please fill the all entry field correctly")
                else:
                    try:
                        email=self.entry_username.get()
                        nvpass=self.new_pass.get()
                        msg = f"~{email},{nvpass}"
                        self.client_socket.send(msg.encode('utf-8'))

                        messagebox.showinfo("Successful", "Password has changed successfully")
                        self.reset_fields()
                        self.root.destroy()

                    except Exception as er:
                        messagebox.showerror("Error!", f"{er}")
         

    def create_widgets(self):
        
        self.frame1 = Frame(self.root, bg="burlywood2")
        self.frame1.place(x=0, y=0, width=450, relheight=1)

        self.image = ImageTk.PhotoImage(file="/home/zkerroumi42/GPT_4UP/Images/logo.jpeg")
        self.image_label = Label(self.frame1, image=self.image, bg="burlywood2")
        self.image_label.place(x=0, y=0)

        self.frame2 = Frame(self.root, bg="old lace")
        self.frame2.place(x=450, y=0, relwidth=1, relheight=1)

        self.frame3 = Frame(self.frame2, bg="burlywood2")
        self.frame3.place(x=140, y=150, width=500, height=450)

        self.username = Label(self.frame3, text="Username", font=("helvetica", 20, "bold"), bg="burlywood2", fg="gray").place(x=50, y=40)
        self.entry_username = Entry(self.frame3, font=("times new roman", 15, "bold"), bg="white", fg="gray")
        self.entry_username.place(x=50, y=80, width=300)

        self.password = Label(self.frame3, text="Password", font=("helvetica", 20, "bold"), bg="burlywood2", fg="gray").place(x=50, y=120)
        self.entry_password = Entry(self.frame3, font=("times new roman", 15, "bold"), bg="white", fg="gray", show="*")
        self.entry_password.place(x=50, y=160, width=300)

        self.btn_login = Button(self.frame3, text="Login",command=self.login, font=("times new roman", 15, "bold"), bd=0, cursor="hand2", bg="burlywood3", fg="black").place(x=50, y=200, width=300)
        
        self.forgotten_pass = Button(self.frame3, text="Forgotten password?",command=self.forgot_func, font=("times new roman", 10, "bold"), bd=0, cursor="hand2", bg="burlywood2", fg="black").place(x=125, y=260, width=150)

        self.btn_register = Button(self.frame3, text="SIGN UP",command=self.switch_to_signup, font=("times new roman", 18, "bold"), bd=0, cursor="hand2", bg="floral white", fg="black").place(x=80, y=320, width=250)
