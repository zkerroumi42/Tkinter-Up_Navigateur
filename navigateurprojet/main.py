import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
from tkinter import filedialog
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tkhtmlview import HTMLLabel
from bs4 import BeautifulSoup
import numpy as np

class ImageClassifierApp:
    def clean_html(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        cleaned_text = soup.get_text(separator='\n', strip=True)
        return cleaned_text

    def __init__(self, master):

        self.master = master
        self.master.title("Image Classifier")
        self.master.geometry("1280x800+0+0")

        # Main Frame
        self.main_frame = tk.Frame(self.master, bg="burlywood2")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Entry widget for text input
        self.text_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.text_entry.pack(pady=10,padx=5)

        # Search Text Button
        search_text_button = tk.Button(self.main_frame, text="Search Text", command=self.search_text, font=("Arial", 12))
        search_text_button.pack()

        # MobileNetV2 Model
        self.model = MobileNetV2(weights='imagenet')

        # Image Label
        self.image_label = tk.Label(self.main_frame)
        self.image_label.pack(pady=10)

        # Browse Image Button
        browse_button = tk.Button(self.main_frame, text="Browse Image", command=self.load_image, font=("Arial", 12))
        browse_button.pack()

        # Classify Image Button
        classify_button = tk.Button(self.main_frame, text="Classify Image", command=self.classify_image, font=("Arial", 12))
        classify_button.pack()

        # Result Label
        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Result Text Widget
        self.result_text_widget = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, width=80, height=10, font=("Arial", 12))
        self.result_text_widget.pack(fill=tk.BOTH, expand=True, pady=10)

        # Initially hide the result text widget
        self.result_text_widget.pack_forget()

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

        # Additional code related to image display if needed

    def search_text(self):
        # Additional code related to searching text if needed

        # Show the result text widget
        self.result_text_widget.pack()

    def classify_image(self):
        # Additional code related to classifying image if needed

        # Show the result text widget
        self.result_text_widget.pack()

# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClassifierApp(root)
    root.mainloop()
