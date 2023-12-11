import socket
import tkinter as tk
from tkinter import messagebox
import threading

class LoginFrame(tk.Frame):
    def __init__(self, root, client_socket):
        super().__init__(root)
        self.root = root
        self.client_socket = client_socket
        self.create_widgets()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        msg = f"#{username},{password}"
        self.client_socket.send(msg.encode('utf-8'))

    def create_widgets(self):
        self.entry_username = tk.Entry(self, width=20)
        self.entry_password = tk.Entry(self, width=20, show='*')
        btn_login = tk.Button(self, text="Login", command=self.login)

        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        btn_login.grid(row=4, column=0, pady=10)

class SignupFrame(tk.Frame):
    def __init__(self, root, client_socket):
        super().__init__(root)
        self.root = root
        self.client_socket = client_socket
        self.create_widgets()

    def signup(self):
        username = self.entry_username.get()
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        password = self.entry_password.get()

        if not username or not nom or not prenom or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        msg = f"+{username},{nom},{prenom},{password}"
        self.client_socket.send(msg.encode('utf-8'))

    def create_widgets(self):
        self.entry_username = tk.Entry(self, width=20)
        self.entry_nom = tk.Entry(self, width=20)
        self.entry_prenom = tk.Entry(self, width=20)
        self.entry_password = tk.Entry(self, width=20, show='*')
        btn_signup = tk.Button(self, text="Sign Up", command=self.signup)

        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_nom.grid(row=2, column=1, padx=10, pady=5)
        self.entry_prenom.grid(row=3, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        btn_signup.grid(row=4, column=1, pady=10)

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Navigateur4UP")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 12345
        self.HOST = socket.gethostbyname(socket.gethostname())
        self.client_socket.connect((self.HOST, self.port))

        recv_msg = self.client_socket.recv(1024).decode('utf-8')
        self.text_messages = tk.Text(self, height=10, width=50, state=tk.DISABLED)
        self.text_messages.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.text_messages.config(state=tk.NORMAL)
        self.text_messages.insert(tk.END, recv_msg + '\n')
        self.text_messages.config(state=tk.DISABLED)

        login_frame = LoginFrame(self, self.client_socket)
        login_frame.grid(row=0, column=0)

        signup_frame = SignupFrame(self, self.client_socket)
        signup_frame.grid(row=1, column=0)

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                recv_msg = self.client_socket.recv(1024).decode('utf-8')
                self.text_messages.config(state=tk.NORMAL)
                self.text_messages.insert(tk.END, recv_msg + '\n')
                self.text_messages.config(state=tk.DISABLED)
            except Exception as e:
                print(str(e))
                break

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
