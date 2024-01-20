import tkinter as tk
import socket
import threading

from login_frame import LoginFrame
from signup_frame import SignupFrame
from dashboard import Dashboard

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GPT4UP")
        self.geometry("1280x800+0+0")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port= 12345
        self.HOST="100.76.26.44"
        # self.HOST=socket.gethostbyname(socket.gethostname())

        self.client_socket.connect((self.HOST, self.port))

        recv_msg = self.client_socket.recv(1024).decode('utf-8')
        print(recv_msg)
        self.current_frame = None
        self.switch_to_login()

    def switch_to_login(self):
        if self.current_frame:
            self.current_frame.destroy()

        login_frame = LoginFrame(self, self.client_socket, self.switch_to_signup, self.switch_to_dashboard)
        login_frame.grid(row=0, column=0)
        self.current_frame = login_frame

    def switch_to_signup(self):
        if self.current_frame:
            self.current_frame.destroy()

        signup_frame = SignupFrame(self, self.client_socket, self.switch_to_login)
        signup_frame.grid(row=1, column=0)
        self.current_frame = signup_frame


    def switch_to_dashboard(self):
      if self.current_frame:
        self.current_frame.destroy()

        dashboard_frame = Dashboard(self, self.client_socket, self.switch_to_login)
        dashboard_frame.pack()
        self.current_frame = dashboard_frame

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        
    def receive_messages(self):
        while True:
            try:

                recv_msg = self.client_socket.recv(1024).decode('utf-8')
                print(recv_msg)

            except Exception as e:
                print(str(e))
                break

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()