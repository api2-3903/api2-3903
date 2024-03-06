import tkinter.simpledialog as simpledialog
import sqlite3
import os
import random
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from database_handler import DatabaseHandler
import pygame
from shutil import copy2
import requests
from gradio_client import Client
import replicate

# Constants
WINDOW_TITLE = 'Wardrobe App'
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
IMG_HEIGHT = 200
IMG_WIDTH = 200
BEIGE_COLOR_HEX = '#E3C396'
SOUND_EFFECT_FILE_PATH = 'assets/yes-2.wav'
REMOVE_BG_API_KEY = 'sHJ7NEaDXAFdLcVDAp11gEvC'  # remove.bg API key

# Collect all clothes (ensure correct path format)
TOPS_FOLDER = "tops"
BOTTOMS_FOLDER = "bottoms"
ALL_TOPS = [f"{TOPS_FOLDER}/{file}" for file in os.listdir(TOPS_FOLDER) if not file.startswith('.')]
ALL_BOTTOMS = [f"{BOTTOMS_FOLDER}/{file}" for file in os.listdir(BOTTOMS_FOLDER) if not file.startswith('.')]
SAVED_OUTFITS_FOLDER = "saved"

#user data (will come from profile page later)
User_gender = "girl" # girl, boy, man, woman
# User_age = "20"
# User_height = "170" //not dealing in absolutes as it doesn't make sense in image generation
# User_weight = "50"
User_body_type = "slim" #slim, normal, fat
User_age = "teen" # old, young, adult, kid, baby 
User_height = " " # short, medium, tall
User_weight = " " # underweight, normal, plus size 

#these attributes come from profile database under advance section only and will be picked up by AI 
# User_skin = "white" # white, black, asian, hispanic,
# User_eyes = "brown eyes" # brown eyes, blue eyes, green eyes, hazel eyes, black eyes
# User_ethnicity = "white" # white, black, asian, hispanic,
# User_glasses = " " # glasses , " "
# User_facial_hair = " " # beard , moustace, goatee , " "
# User_hair_length = "shoulder length hair" # shoulder length hair,  short hair , long hair
# User_hair_color = "black hair" # Ginger hair, brown hair, blonde hair, blue hair
# User_hair_style = "straight hair" #curly hair, wavy hair

#these attributes come from clothes database 
User_top_style = "casual" # formal, casual 
User_bottom_style = "casual" # formal, casual
User_top_color = "black" # black, white, red, blue,
User_bottom_color = "black" # black, white, red, blue,




class AutocompleteEntry(tk.Entry):
    def __init__(self, *args, completions=None, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.completions = completions
        if self.completions is None:
            self.completions = []

        self.autocomplete_list = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)

    def autocomplete(self, delta=0):
        # Get the current text in the entry
        current_text = self.get()

        # Clear previous autocompletion suggestions
        self.autocomplete_list = []

        # If there is text in the entry, find matching suggestions
        if current_text:
            current_text_lower = current_text.lower()
            self.autocomplete_list = [word for word in self.completions if current_text_lower in word.lower()]

        # If there are matching suggestions, show the first one
        if self.autocomplete_list:
            self.delete(0, tk.END)
            self.insert(0, self.autocomplete_list[0])
            self.select_range(len(current_text), tk.END)

    def handle_keyrelease(self, event):
        # Handle key release events
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift', 'Control'):
            # Ignore certain keys
            return
        self.autocomplete()

    def set_completions(self, completions):
        self.completions = completions


class AutocompleteEntryDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, completion_list):
        self.prompt = prompt
        self.completion_list = completion_list
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text=self.prompt).grid(row=0)
        self.entry = AutocompleteEntry(master, completions=self.completion_list)
        self.entry.grid(row=0, column=1)
        return self.entry

    def apply(self):
        self.result = self.entry.get()


class WardrobeApp:
    def __init__(self, root, db_handler):
        self.root = root
        self.db_handler = db_handler
        self.top_images = ALL_TOPS
        self.bottom_images = ALL_BOTTOMS
        self.tops_image_path = self.top_images[0]
        self.bottom_image_path = self.bottom_images[0]

        # self.all_tops_list = ["Top1", "Top2", "Top3"]  # trial
        # self.all_bottoms_list = ["Bottom1", "Bottom2", "Bottom3"]  

         # Fetch all top names and bottom names from the database
        self.all_tops_list = self.db_handler.get_all_top_names()
        self.all_bottoms_list = self.db_handler.get_all_bottom_names()


        self.all_sizes_list = ["XS", "S", "M", "L", "XL", "XXL","XXXL"]
        self.all_colors_list = ["Red", "Blue", "Green", "Yellow", "Black", "White", "Orange", "Purple", "Brown", "Pink", "Grey","Gold", "Silver","Maroon","Dark Blue", "Dark Green", "Dark Red"]
        self.all_fabrics_list = ["Cotton", "Wool", "Silk", "Leather", "Nylon", "Polyester", "Linen", "Cashmere", "Denim","Rayon"]
        self.all_styles_list = ["Casual", "Formal", "Sporty", "Skater", "Business", "Ethnic","Street"]
        self.all_seasons_list = ["Spring", "Summer", "Fall", "Winter"]
        self.all_brands_list = ["Levi's", "H&M", "Gap", "American Eagle", "Old Navy", "Abercrombie & Fitch", "Forever 21", "Zara", "Uniqlo", "Urban Outfitters",
                        "Hugo Boss", "Ralph Lauren", "Calvin Klein", "Brooks Brothers", "Armani", "Tommy Hilfiger", "Gucci", "Burberry", "Dolce & Gabbana", "Versace",
                        "Nike", "Adidas", "Under Armour", "Puma", "Reebok", "New Balance", "Champion", "Fila", "ASICS", "Lululemon","Converse",
                        "Vans", "DC Shoes", "Element", "Etnies", "Globe", "Volcom", "Santa Cruz Skateboards", "Primitive Skateboarding", "Lakai", "Huf",
                        "Brooks Brothers", "Hugo Boss", "Ralph Lauren", "Calvin Klein", "Armani", "Tommy Hilfiger", "Gucci", "Burberry", "Dolce & Gabbana", "Versace",
                        "Desigual", "Natori", "Missoni", "Fendi", "Etro", "Anna Sui", "Diane von Furstenberg", "Valentino", "Givenchy", "Roberto Cavalli",
                        "Highlander","Supreme", "Off-White", "Bape", "Palace Skateboards", "Stussy", "Kith", "Yeezy", "Fear of God", "Vetements", "Palace"]



        self.tops_frame = tk.Frame(self.root, bg=BEIGE_COLOR_HEX)
        self.bottoms_frame = tk.Frame(self.root, bg=BEIGE_COLOR_HEX)

        self.top_image_label = self.create_photo(self.tops_image_path, self.tops_frame)
        self.top_image_label.pack(side=tk.TOP)

        self.bottom_image_label = self.create_photo(self.bottom_image_path, self.bottoms_frame)
        self.bottom_image_label.pack(side=tk.TOP)

        self.top_name_combobox = ttk.Combobox(self.tops_frame, values=self.all_tops_list)
        self.bottom_name_combobox = ttk.Combobox(self.bottoms_frame, values=self.all_bottoms_list)

        self.all_sizes_combobox = ttk.Combobox(self.tops_frame, values=self.all_sizes_list)
        self.all_colors_combobox = ttk.Combobox(self.bottoms_frame, values=self.all_colors_list)
        self.all_fabrics_combobox = ttk.Combobox(self.tops_frame, values=self.all_fabrics_list)
        self.all_styles_combobox = ttk.Combobox(self.bottoms_frame, values=self.all_styles_list)
        self.all_brands_combobox = ttk.Combobox(self.tops_frame, values=self.all_brands_list)
        

        self.create_background()

    def create_background(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
        self.create_buttons()
        self.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)

    def on_close(self):
        self.db_handler.close_connection()
        self.root.destroy()
        print("closing")

    # def create_outfit(self):
    #     try:
    #         new_top_index = random.randint(0, len(self.top_images) - 1)
    #         new_bottom_index = random.randint(0, len(self.bottom_images) - 1)

    #         self.update_photo(self.top_images[new_top_index], self.top_image_label)
    #         self.update_photo(self.bottom_images[new_bottom_index], self.bottom_image_label)

    #         pygame.mixer.init()
    #         pygame.mixer.music.load(SOUND_EFFECT_FILE_PATH)
    #         pygame.mixer.music.play()
    #     except Exception as e:
    #         print(f"Error creating outfit: {e}")
        
    def create_outfit(self):
        try:
            # Select random top and bottom images
            new_top_index = random.randint(0, len(self.top_images) - 1)
            new_bottom_index = random.randint(0, len(self.bottom_images) - 1)
            top_image_path = self.top_images[new_top_index]
            bottom_image_path = self.bottom_images[new_bottom_index]

             # Fetch top and bottom styles and colors from the database
            User_top_style = self.db_handler.get_top_style_by_path(top_image_path)
            User_top_color = self.db_handler.get_top_color_by_path(top_image_path)
            User_bottom_style = self.db_handler.get_bottom_style_by_path(bottom_image_path)
            User_bottom_color = self.db_handler.get_bottom_color_by_path(bottom_image_path)

            #dynamic prompt template
            prompt_template = f"# {User_age} {User_height} {User_weight} {User_body_type} {User_gender}  wearing"
            if User_top_style:
                prompt_template += f" {User_top_style}"
            if User_bottom_style:
                prompt_template += f" {User_bottom_style}"
            prompt_template += " with"
            if User_top_color:
                prompt_template += f" {User_top_color}"
            if User_bottom_color:
                prompt_template += f" {User_bottom_color}"
            prompt_template += " clothes"

            # Send top and bottom images to Gradio API (replaced due to poor API Health)
            # gr = Client(api_key="https://cc1808eeb7bcd9c0cd.gradio.live/")
            # output_image = gr.predict(top_image_path, bottom_image_path)
            

            output_image_temp = replicate.run(
            "konieshadow/fooocus-api-realistic:8958d6f677f825b57175bf644471fddfee6210a165cc20037323575a84d16afb",
            input={
                    "prompt": prompt_template,
                    "cn_img1": top_image_path,
                    "cn_stop1": 0.81,
                    "cn_weight1" : 1.1,
                    "cn_type1": "ImagePrompt",
                    "cn_img2": bottom_image_path,
                    "cn_stop2": 0.81,
                    "cn_weight2": 1.1,
                    "cn_type2": "ImagePrompt",
                    "cn_type3": "ImagePrompt",
                    "cn_type4": "ImagePrompt",
                    "sharpness": 2,
                    "image_seed": -1,
                    "uov_method": "Disabled",
                    "image_number": 1,
                    "guidance_scale": 3,
                    "refiner_switch": 0.5,
                    "negative_prompt": "unrealistic,mutilated pupils,saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
                    "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
                    "uov_upscale_value": 0,
                    "outpaint_selections": "",
                    "outpaint_distance_top": 0,
                    "performance_selection": "Speed",
                    "outpaint_distance_left": 0,
                    "aspect_ratios_selection": "768*1344",
                    "outpaint_distance_right": 0,
                    "outpaint_distance_bottom": 0,
                    "inpaint_additional_prompt": ""
                }
            )

            output_image = replicate.run(
            "konieshadow/fooocus-api-realistic:8958d6f677f825b57175bf644471fddfee6210a165cc20037323575a84d16afb",
            input={
                    "prompt": prompt_template,
                    "cn_img1": top_image_path,
                    "cn_stop1": 0.41,
                    "cn_weight1" : 0.5,
                    "cn_type1": "ImagePrompt",
                    "cn_img2": bottom_image_path,
                    "cn_stop2": 0.41,
                    "cn_weight2": 0.5,
                    "cn_type2": "ImagePrompt",
                    "cn_type3": "ImagePrompt",
                    "cn_type4": "ImagePrompt",
                    "sharpness": 2,
                    "image_seed": -1,
                    "uov_method": "Disabled",
                    "image_number": 1,
                    "guidance_scale": 3,
                    "refiner_switch": 0.5,
                    "negative_prompt": "unrealistic,mutilated pupils,saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
                    "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
                    "uov_upscale_value": 0,
                    "outpaint_selections": "",
                    "outpaint_distance_top": 0,
                    "performance_selection": "Speed",
                    "outpaint_distance_left": 0,
                    "aspect_ratios_selection": "768*1344",
                    "outpaint_distance_right": 0,
                    "outpaint_distance_bottom": 0,
                    "inpaint_additional_prompt": ""
                }
            )

            # Display the rendered outfit image
            self.update_photo(output_image, self.top_image_label)

            # Play sound effect
            pygame.mixer.init()
            pygame.mixer.music.load(SOUND_EFFECT_FILE_PATH)
            pygame.mixer.music.play()

        except Exception as e:
            print(f"Error creating outfit: {e}")


    def create_buttons(self):
        button_params = [
            (self.tops_frame, "Prev", self.get_prev_top, tk.LEFT),
            (self.tops_frame, "Create Outfit", self.create_outfit, tk.LEFT),
            (self.tops_frame, "Next", self.get_next_top, tk.RIGHT),
            (self.bottoms_frame, "Prev", self.get_prev_bottom, tk.LEFT),
            (self.bottoms_frame, "Next", self.get_next_bottom, tk.RIGHT),
            (self.bottoms_frame, "Upload Bottom", self.upload_bottom, tk.RIGHT),
            (self.tops_frame, "Upload Top", self.upload_top, tk.RIGHT),
            (self.tops_frame, "Save Outfit", self.save_outfit, tk.RIGHT),
        ]

        for frame, text, command, side in button_params:
            button = tk.Button(frame, text=text, command=command)
            button.pack(side=side)

    def create_photo(self, image, frame):
        top_image_file = Image.open(image)
        image = top_image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, anchor=tk.CENTER)
        image_label.image = photo
        return image_label

    def update_photo(self, new_image, image_label):
        new_image_file = Image.open(new_image)
        image = new_image_file.resize((IMG_WIDTH, IMG_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.configure(image=photo)
        image_label.image = photo

    def _get_next_item(self, current_item, category, increment=True):
        item_index = category.index(current_item)
        final_index = len(category) - 1
        next_index = 0

        if increment and item_index == final_index:
            next_index = 0
        elif not increment and item_index == 0:
            next_index = final_index
        else:
            incrementor = 1 if increment else -1
            next_index = item_index + incrementor

        next_image = category[next_index]

        if current_item in self.top_images:
            image_label = self.top_image_label
            self.tops_image_path = next_image
            self.top_name_combobox.set(next_image)
        else:
            image_label = self.bottom_image_label
            self.bottom_image_path = next_image
            self.bottom_name_combobox.set(next_image)

        self.update_photo(next_image, image_label)

    def get_next_top(self):
        self._get_next_item(self.tops_image_path, self.top_images, increment=True)

    def get_prev_top(self):
        self._get_next_item(self.tops_image_path, self.top_images, increment=False)

    def get_prev_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.bottom_image_path, self.bottom_images, increment=True)

    def upload_image(self, folder):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            return file_path
        return None

    def remove_background(self, image_path):
        try:
            api_url = "https://api.remove.bg/v1.0/removebg"
            headers = {
                "X-Api-Key": REMOVE_BG_API_KEY,
            }
            input_path = os.path.abspath(image_path)
            output_path = os.path.join(os.path.dirname(input_path), "output.png")
            files = {
                'image_file': open(input_path, 'rb'),
            }
            response = requests.post(api_url, headers=headers, files=files)

            if response.status_code == 200:
                with open(output_path, 'wb') as output_file:
                    output_file.write(response.content)
                return output_path
            else:
                print(f"Error removing background: {response.text}")

        except Exception as e:
            print(f"Error removing background: {e}")

        return None

    def show_autocomplete_dialog(self, prompt, completion_list, combobox):
        dialog = AutocompleteEntryDialog(self.root, "Enter Name", prompt, completion_list)
        dialog_result = dialog.result

        if dialog_result:
            combobox.set(dialog_result)

    def upload_top(self):
        new_top_path = self.upload_image(TOPS_FOLDER)
        if new_top_path:
            self.show_autocomplete_dialog("Enter the name for the top:", self.all_tops_list, self.top_name_combobox)
            self.show_autocomplete_dialog("Enter the size for the top:", self.all_sizes_list, self.all_sizes_combobox)
            self.show_autocomplete_dialog("Enter the color for the top:", self.all_colors_list, self.all_colors_combobox)
            self.show_autocomplete_dialog("Enter the brand for the top:", self.all_brands_list, self.all_brands_combobox)
            self.show_autocomplete_dialog("Enter the genre for the top:", self.all_styles_list, self.all_styles_combobox)
            self.show_autocomplete_dialog("Enter the fabric for the top:", self.all_fabrics_list, self.all_fabrics_combobox)
            
            # top_size = simpledialog.askstring("Input", "Enter the size for the top:")
            # top_color = simpledialog.askstring("Input", "Enter the color for the top:")
            # top_brand = simpledialog.askstring("Input", "Enter the brand for the top:")
            # top_genre = simpledialog.askstring("Input", "Enter the genre for the top:")
            # top_fabric = simpledialog.askstring("Input", "Enter the fabric for the top:")

            new_top_path_no_bg = self.remove_background(new_top_path)

            if new_top_path_no_bg:
                new_top_path_no_bg_renamed = os.path.join(TOPS_FOLDER, f"{self.top_name_combobox.get()}.png")
                os.rename(new_top_path_no_bg, new_top_path_no_bg_renamed)
                self.store_clothing_details(self.top_name_combobox.get(), "top", self.all_sizes_combobox.get(), self.all_colors_combobox.get(), self.all_brands_combobox.get(), self.all_styles_combobox.get(),self.all_fabrics_combobox.get(),new_top_path_no_bg)
                self.top_images = [new_top_path_no_bg_renamed] + ALL_TOPS[1:]
                self.tops_image_path = new_top_path_no_bg_renamed
                self.update_photo(new_top_path_no_bg_renamed, self.top_image_label)
                self.top_name_combobox['values'] = self.all_tops_list

    def upload_bottom(self):
        new_bottom_path = self.upload_image(BOTTOMS_FOLDER)
        if new_bottom_path:
            self.show_autocomplete_dialog("Enter the name for the bottom:", self.all_bottoms_list, self.bottom_name_combobox)
            self.show_autocomplete_dialog("Enter the size for the bottom:", self.all_sizes_list, self.all_sizes_combobox)
            self.show_autocomplete_dialog("Enter the color for the bottom:", self.all_colors_list, self.all_colors_combobox)
            self.show_autocomplete_dialog("Enter the brand for the bottom:", self.all_brands_list, self.top_name_combobox)
            self.show_autocomplete_dialog("Enter the genre for the bottom:", self.all_styles_list, self.all_brands_combobox)
            self.show_autocomplete_dialog("Enter the fabric for the bottom:", self.all_fabrics_list, self.all_fabrics_combobox)


            # bottom_size = simpledialog.askstring("Input", "Enter the size for the bottom:")
            # bottom_color = simpledialog.askstring("Input", "Enter the color for the bottom:")
            # bottom_brand = simpledialog.askstring("Input", "Enter the brand for the bottom:")
            # bottom_genre = simpledialog.askstring("Input", "Enter the genre for the bottom:")
            # bottom_fabric = simpledialog.askstring("Input", "Enter the fabric for the bottom:")

            new_bottom_path_no_bg = self.remove_background(new_bottom_path)

            if new_bottom_path_no_bg:
                new_bottom_path_no_bg_renamed = os.path.join(BOTTOMS_FOLDER, f"{self.bottom_name_combobox.get()}.png")
                os.rename(new_bottom_path_no_bg, new_bottom_path_no_bg_renamed)
                self.store_clothing_details(self.bottom_name_combobox.get(), "bottom", self.all_sizes_combobox.get(), self.all_colors_combobox.get(), self.all_brands_combobox.get(), self.all_styles_combobox.get(),self.all_fabrics_combobox.get(),new_bottom_path_no_bg)
                self.bottom_images = [new_bottom_path_no_bg_renamed] + ALL_BOTTOMS[1:]
                self.bottom_image_path = new_bottom_path_no_bg_renamed
                self.update_photo(new_bottom_path_no_bg_renamed, self.bottom_image_label)
                self.bottom_name_combobox['values'] = self.all_bottoms_list

    def store_clothing_details(self, name, clothing_type, size, color, brand, genre, fabric,path):
        try:
            self.db_handler.store_clothing_details(name, clothing_type, size, color, brand, genre, fabric,path)
        except Exception as e:
            print(f"Error storing clothing details: {e}")

    def save_outfit(self):
        saved_outfits_path = os.path.join(os.getcwd(), SAVED_OUTFITS_FOLDER)
        os.makedirs(saved_outfits_path, exist_ok=True)

        outfit_name = filedialog.asksaveasfilename(
            initialdir=saved_outfits_path,
            title="Save Outfit",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")],
            defaultextension=".png",
        )

        if outfit_name:
            copy2(self.tops_image_path, os.path.join(saved_outfits_path, f"{outfit_name}_top.png"))
            copy2(self.bottom_image_path, os.path.join(saved_outfits_path, f"{outfit_name}_bottom.png"))


if __name__ == '__main__':
    root = tk.Tk()
    db_handler = DatabaseHandler("wardrobe_database.db")
    app = WardrobeApp(root, db_handler)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
