import socket
import tkinter as tk
from tkinter import messagebox
import threading

def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required.")
        return

    msg = f"#{username}{password}"
    client_socket.send(msg.encode('utf-8'))

def signup():
    username = entry_username.get()
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    password = entry_password.get()

    if not username or not nom or not prenom or not password:
        messagebox.showerror("Error", "All fields are required.")
        return

    msg = f"+{username}{nom}{prenom}{password}"
    client_socket.send(msg.encode('utf-8'))

def receive_messages():
    while True:
        try:
            recv_msg = client_socket.recv(1024).decode('utf-8')
            text_messages.config(state=tk.NORMAL)
            text_messages.insert(tk.END, recv_msg + '\n')
            text_messages.config(state=tk.DISABLED)
        except Exception as e:
            print(str(e))
            break

# Create the main window
root = tk.Tk()
root.title("Chat Application")

# Create and configure GUI elements
entry_username = tk.Entry(root, width=20)
entry_password = tk.Entry(root, width=20, show='*')
entry_nom = tk.Entry(root, width=20)
entry_prenom = tk.Entry(root, width=20)
btn_login = tk.Button(root, text="Login", command=login)
btn_signup = tk.Button(root, text="Sign Up", command=signup)
text_messages = tk.Text(root, height=10, width=50, state=tk.DISABLED)

# Place GUI elements on the window
entry_username.grid(row=0, column=1, padx=10, pady=5)
entry_password.grid(row=1, column=1, padx=10, pady=5)
entry_nom.grid(row=2, column=1, padx=10, pady=5)
entry_prenom.grid(row=3, column=1, padx=10, pady=5)
btn_login.grid(row=4, column=0, pady=10)
btn_signup.grid(row=4, column=1, pady=10)
text_messages.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Initialize the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345
HOST = socket.gethostbyname(socket.gethostname())
client_socket.connect((HOST, port))

# Receive connection message from the server
recv_msg = client_socket.recv(1024).decode('utf-8')
text_messages.config(state=tk.NORMAL)
text_messages.insert(tk.END, recv_msg + '\n')
text_messages.config(state=tk.DISABLED)

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Run the Tkinter event loop
root.mainloop()
