from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import  ImageTk


from tkinter import messagebox


class SignupFrame(tk.Frame):
    def __init__(self, root, client_socket, switch_to_login_callback):
        super().__init__(root)
        self.root = root
        self.root
        self.client_socket = client_socket
        self.switch_to_login_callback = switch_to_login_callback
        self.create_widgets()

    def signup(self):
        username = self.entry_username.get()
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        password = self.entry_password.get()
        question=self.questions.get()
        answer=self.answer_txt.get()

        if not username or not nom or not prenom or not password or not question or not answer:
            messagebox.showerror("Error", "All fields are required.")
            return

        msg = f"+{username},{nom},{prenom},{password},{question},{answer}"
        self.client_socket.send(msg.encode('utf-8'))
        self.reset_fields()
        print(username,nom,prenom,password,question,answer)
        self.switch_to_login()

    def switch_to_login(self):
        self.switch_to_login_callback()

    def reset_fields(self):
        self.entry_username.delete(0, END)
        self.entry_nom.delete(0, END)
        self.entry_prenom.delete(0, END)
        self.entry_password.delete(0,END)

    def create_widgets(self):
        
    
        self.bg_img = ImageTk.PhotoImage(file="Images/fst.jpg")
        background = Label(self.root,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)


        frame = Frame(self.root, bg="burlywood2")
        frame.place(x=350,y=100,width=500,height=550)

        title1 = Label(frame, text="Sign Up", font=("times new roman",25,"bold"),bg="burlywood2").place(x=20, y=10)
        title2 = Label(frame, text="Join with us", font=("times new roman",13),bg="burlywood2", fg="gray").place(x=20, y=50)

        lblnom = Label(frame, text="Nom ", font=("helvetica",15,"bold"),bg="burlywood2").place(x=20, y=100)
        lblprenom = Label(frame, text="Prenom", font=("helvetica",15,"bold"),bg="burlywood2").place(x=240, y=100)

        self.entry_nom = Entry(frame,font=("arial"))
        self.entry_nom.place(x=20, y=130, width=200)

        self.entry_prenom = Entry(frame,font=("arial"))
        self.entry_prenom.place(x=240, y=130, width=200)

        email = Label(frame, text="Email", font=("helvetica",15,"bold"),bg="burlywood2").place(x=20, y=180)

        self.entry_username = Entry(frame,font=("arial"))
        self.entry_username.place(x=20, y=210, width=420)

        sec_question = Label(frame, text="Security questions", font=("helvetica",15,"bold"),bg="burlywood2").place(x=20, y=260)
        answer = Label(frame, text="Answer", font=("helvetica",15,"bold"),bg="burlywood2").place(x=240, y=260)

        self.questions = ttk.Combobox(frame,font=("helvetica",13),state='readonly',justify=CENTER)
        self.questions['values'] = ("Select","What's your pet name?","Your first teacher name","Your birthplace", "Your favorite movie")
        self.questions.place(x=20,y=290,width=200)
        self.questions.current(0)


       
        self.answer_txt = Entry(frame,font=("arial"))
        self.answer_txt.place(x=240, y=290, width=200)

        lblpassword =  Label(frame, text="Password", font=("helvetica",15,"bold"),bg="burlywood2").place(x=20, y=340)

        self.entry_password = Entry(frame,font=("arial"),show="*")
        self.entry_password.place(x=20, y=370, width=420)

        self.terms = IntVar()
        box = Checkbutton(frame,text="I Agree The Terms & Conditions",variable=self.terms,onvalue=1,offvalue=0,bg="burlywood2",font=("times new roman",12)).place(x=20,y=420)
        self.signup = Button(frame,text="Sign Up",command=self.signup,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="burlywood3",fg="black").place(x=120,y=470,width=250)