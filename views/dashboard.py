import socket
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from PIL import Image, ImageTk
import threading
import requests
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from tkhtmlview import HTMLLabel
from bs4 import BeautifulSoup
import numpy as np
from tkinter import messagebox

class Dashboard(tk.Frame):
    def clean_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        cleaned_text = soup.get_text(separator='\n', strip=True)
        return cleaned_text

    def __init__(self, root, client_socket, switch_to_login_callback):
        super().__init__(root)
        self.root = root
        self.client_socket = client_socket
        self.switch_to_login_callback = switch_to_login_callback
        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("750x800")

        header_frame = Frame(self, bg="burlywood2")
        header_frame.pack(fill=X)

        header_image = Image.open("/home/zkerroumi42/GPT_4UP/Images/nav.png")
        header_image = ImageTk.PhotoImage(header_image)
        header_label = Label(header_frame, image=header_image, bg='burlywood2')
        header_label.image = header_image
        header_label.pack(pady=10)

        content_frame = Frame(self, bg="burlywood2")
        content_frame.pack(fill=BOTH, expand=True)

        self.text_entry = Entry(content_frame, font=("Arial", 14))
        self.text_entry.pack(pady=10, padx=10, fill=X, expand=True)

        button_frame = Frame(content_frame, bg="burlywood2")
        button_frame.pack(pady=10, padx=10, fill=X)

        search_text_button = Button(button_frame, text="Search Text", command=self.search_text, font=("Arial", 12))
        search_text_button.pack(side=LEFT, padx=5)

        classify_button = Button(button_frame, text="Classify Image", command=self.classify_image, font=("Arial", 12))
        classify_button.pack(side=LEFT, padx=5)

        browse_button = Button(button_frame, text="Browse Image", command=self.load_image, font=("Arial", 12))
        browse_button.pack(side=LEFT, padx=5)

        self.model = MobileNetV2(weights='imagenet')

        self.image_label = Label(content_frame)
        self.image_label.pack(pady=10)

        self.result_label = Label(content_frame, text="")
        self.result_label.pack()

        canvas = Canvas(content_frame, bg="burlywood2")
        scroll_y = Scrollbar(content_frame, orient="vertical", command=canvas.yview)

        text_frame = Frame(canvas, bg="burlywood2")

        self.result_text_widget = scrolledtext.ScrolledText(text_frame, wrap=WORD, width=80, height=20, font=("Arial", 12))
        self.result_text_widget.pack(fill=BOTH, expand=True, pady=10)

        canvas.create_window((0, 0), window=text_frame, anchor="nw")
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

        canvas.pack(fill=BOTH, expand=True)
        scroll_y.pack(side=RIGHT, fill=Y)

        text_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        image_data = Image.open(file_path)
        image_data = image_data.resize((300, 300), Image.LANCZOS)
        image_data = ImageTk.PhotoImage(image_data)
        self.image_label.config(image=image_data)
        self.image_label.image = image_data

        self.image_path = file_path
        self.result_label.config(text="")

    def search_google(self, query):
        search_url = f"https://en.wikipedia.org/wiki/{query}"
        response = requests.get(search_url)
        return response.text

    def classify_image(self):
        if hasattr(self, 'image_path'):
            img = image.load_img(self.image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)

            predictions = self.model.predict(img_array)
            decoded_predictions = decode_predictions(predictions, top=1)[0]

            predicted_text = decoded_predictions[0][1]
            confidence = decoded_predictions[0][2]

            result_text = f"Prediction: {predicted_text} ({confidence:.2f})"
            self.result_label.config(text=result_text)
            search_results_html = self.search_google(predicted_text)
            search_results_text = self.clean_html(search_results_html)
            self.result_text_widget.delete(1.0, tk.END)
            self.result_text_widget.insert(tk.END, search_results_text)
            self.root.geometry("750x1200")

        else:
            self.result_label.config(text="Please load an image first.")

    def search_text(self):
        text_query = self.text_entry.get().strip()

        if text_query:
            search_results_html = self.search_google(text_query)
            search_results_text = self.clean_html(search_results_html)
            self.result_text_widget.delete(1.0, tk.END)
            self.result_text_widget.insert(tk.END, search_results_text)
        else:
            self.result_label.config(text="Please enter text for search.")

    def switch_to_login(self):
        self.switch_to_login_callback()


