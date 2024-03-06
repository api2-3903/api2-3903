# image_processing.py
from PIL import Image, ImageTk
from tkinter import tk
from shutil import copy2
import os
import requests
from tkinter import filedialog
from tkinter import simpledialog

class ImageProcessor:
    def __init__(self, tops_folder, bottoms_folder, remove_bg_api_key, sound_effect_file_path):
        self.TOPS_FOLDER = tops_folder
        self.BOTTOMS_FOLDER = bottoms_folder
        self.REMOVE_BG_API_KEY = remove_bg_api_key
        self.SOUND_EFFECT_FILE_PATH = sound_effect_file_path

    def create_photo(self, image, frame, img_width, img_height):
        top_image_file = Image.open(image)
        image = top_image_file.resize((img_width, img_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, anchor=tk.CENTER)
        image_label.image = photo
        return image_label

    def update_photo(self, new_image, image_label, img_width, img_height):
        new_image_file = Image.open(new_image)
        image = new_image_file.resize((img_width, img_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

    def upload_image(self, folder):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            return file_path
        return None

    def remove_background(self, image_path):
        try:
            # Specify remove.bg API endpoint
            api_url = "https://api.remove.bg/v1.0/removebg"

            # Prepare headers with the API key
            headers = {
                "X-Api-Key": self.REMOVE_BG_API_KEY,
            }

            # Specify the input image path and output image path
            input_path = os.path.abspath(image_path)
            output_path = os.path.join(os.path.dirname(input_path), "output.png")

            # Prepare files for the API request
            files = {
                'image_file': open(input_path, 'rb'),
            }

            # Make a POST request to remove.bg API
            response = requests.post(api_url, headers=headers, files=files)

            # Check if the request was successful
            if response.status_code == 200:
                # Save the output image with a transparent background
                with open(output_path, 'wb') as output_file:
                    output_file.write(response.content)

                return output_path

            else:
                print(f"Error removing background: {response.text}")

        except Exception as e:
            print(f"Error removing background: {e}")

        return None
