# wardrobe_ui.py
import os
import tkinter as tk
from tkinter import ttk, simpledialog, filedialog
from PIL import Image, ImageTk
from database_handler import DatabaseHandler
import requests
from tkinter import simpledialog
from autocomplete import AutocompleteEntry 

class WardrobeUI:
    def __init__(self, root, wardrobe_app):
        self.root = root
        self.wardrobe_app = wardrobe_app
        self.create_background()

    def set_autocomplete(self, entry, values):
        """
        Set autocomplete for the given entry widget.
        """
        def autocomplete():
            # Get the current entry value
            current_entry = entry.get().lower()

            # Get matching values from the list
            matching_values = [value for value in values if current_entry in value.lower()]

            # Update the autocompletion list
            entry['values'] = matching_values

        # Bind the autocomplete function to key release event
        entry.bind('<KeyRelease>', lambda event: autocomplete())

    
    class AutocompleteEntryDialog(simpledialog.Dialog):
        def __init__(self, parent, title, prompt, completion_list):
            self.prompt = prompt
            self.completion_list = completion_list
            super().__init__(parent, title)

        def body(self, master):
            tk.Label(master, text=self.prompt).grid(row=0)
            self.entry =  AutocompleteEntry(master)  # Use the correct class name here
            self.entry.grid(row=0, column=1)
            self.set_autocomplete(self.entry, self.completion_list)
            return self.entry

        def apply(self):
            self.result = self.entry.get()



    def create_background(self):
        self.root.title(self.wardrobe_app.root.title())
        self.root.geometry(f'{self.root.winfo_width()}x{self.root.winfo_height()}')
        self.create_buttons()

        tk.Label(self.wardrobe_app.tops_frame, text="Top Name:").pack(side=tk.LEFT, padx=5)
        self.top_name_entry = AutocompleteEntry(self.wardrobe_app.tops_frame)
        self.top_name_entry.pack(side=tk.LEFT, padx=5)
        self.set_autocomplete(self.top_name_entry, self.wardrobe_app.all_tops_list)

        tk.Label(self.wardrobe_app.bottoms_frame, text="Bottom Name:").pack(side=tk.LEFT, padx=5)
        self.bottom_name_entry = AutocompleteEntry(self.wardrobe_app.bottoms_frame)
        self.bottom_name_entry.pack(side=tk.LEFT, padx=5)
        self.set_autocomplete(self.bottom_name_entry, self.wardrobe_app.all_bottoms_list)

        self.wardrobe_app.tops_frame.pack(fill=tk.BOTH, expand=tk.YES)
        self.wardrobe_app.bottoms_frame.pack(fill=tk.BOTH, expand=tk.YES)
    
    def create_buttons(self):
        button_params = [
            (self.wardrobe_app.tops_frame, "Prev", self.wardrobe_app.get_prev_top, tk.LEFT),
            (self.wardrobe_app.tops_frame, "Create Outfit", self.wardrobe_app.create_outfit, tk.LEFT),
            (self.wardrobe_app.tops_frame, "Next", self.wardrobe_app.get_next_top, tk.RIGHT),
            (self.wardrobe_app.bottoms_frame, "Prev", self.wardrobe_app.get_prev_bottom, tk.LEFT),
            (self.wardrobe_app.bottoms_frame, "Next", self.wardrobe_app.get_next_bottom, tk.RIGHT),
            (self.wardrobe_app.bottoms_frame, "Upload Bottom", self.wardrobe_app.upload_bottom, tk.RIGHT),
            (self.wardrobe_app.tops_frame, "Upload Top", self.wardrobe_app.upload_top, tk.RIGHT),
            (self.wardrobe_app.tops_frame, "Save Outfit", self.wardrobe_app.save_outfit, tk.RIGHT),
        ]

        for frame, text, command, side in button_params:
            button = tk.Button(frame, text=text, command=command)
            button.pack(side=side)

    def create_photo(self, image, frame):
        top_image_file = Image.open(image)
        image = top_image_file.resize((self.wardrobe_app.IMG_WIDTH, self.wardrobe_app.IMG_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo, anchor=tk.CENTER)
        image_label.image = photo
        return image_label

    def update_photo(self, new_image, image_label):
        new_image_file = Image.open(new_image)
        image = new_image_file.resize((self.wardrobe_app.IMG_WIDTH, self.wardrobe_app.IMG_HEIGHT), Image.LANCZOS)
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

        if current_item in self.wardrobe_app.top_images:
            image_label = self.wardrobe_app.top_image_label
            self.wardrobe_app.tops_image_path = next_image
        else:
            image_label = self.wardrobe_app.bottom_image_label
            self.wardrobe_app.bottom_image_path = next_image

        self.update_photo(next_image, image_label)

    def get_next_top(self):
        self._get_next_item(self.wardrobe_app.tops_image_path, self.wardrobe_app.top_images, increment=True)

    def get_prev_top(self):
        self._get_next_item(self.wardrobe_app.tops_image_path, self.wardrobe_app.top_images, increment=False)

    def get_prev_bottom(self):
        self._get_next_item(self.wardrobe_app.bottom_image_path, self.wardrobe_app.bottom_images, increment=False)

    def get_next_bottom(self):
        self._get_next_item(self.wardrobe_app.bottom_image_path, self.wardrobe_app.bottom_images, increment=True)

    def upload_image(self, folder):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            return file_path
        return None

    def remove_background(self, image_path):
        try:
            api_url = "https://api.remove.bg/v1.0/removebg"
            headers = {"X-Api-Key": self.wardrobe_app.REMOVE_BG_API_KEY}
            input_path = os.path.abspath(image_path)
            output_path = os.path.join(os.path.dirname(input_path), "output.png")
            files = {'image_file': open(input_path, 'rb')}
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

    def upload_top(self):
        new_top_path = self.upload_image(self.wardrobe_app.TOPS_FOLDER)
        if new_top_path:
            # Get details from the user
            top_name = WardrobeUI.AutocompleteEntryDialog(self.root, "Enter Top Name", "Enter the name for the top:", self.wardrobe_app.all_tops_list).result
            top_size = simpledialog.askstring("Input", "Enter the size for the top:")
            top_color = simpledialog.askstring("Input", "Enter the color for the top:")
            top_brand = simpledialog.askstring("Input", "Enter the brand for the top:")
            top_genre = simpledialog.askstring("Input", "Enter the genre for the top:")
            top_fabric = simpledialog.askstring("Input", "Enter the fabric for the top:")

            # Remove the background from the uploaded top image
            new_top_path_no_bg = self.remove_background(new_top_path)

            if new_top_path_no_bg:
                # Rename the uploaded top image with the user-provided name
                new_top_path_no_bg_renamed = os.path.join(self.wardrobe_app.TOPS_FOLDER, f"{top_name}.png")
                os.rename(new_top_path_no_bg, new_top_path_no_bg_renamed)

                # Store details in the SQLite database
                self.wardrobe_app.store_clothing_details(top_name, "top", top_size, top_color, top_brand, top_genre, top_fabric)

                self.wardrobe_app.top_images = [new_top_path_no_bg_renamed] + self.wardrobe_app.ALL_TOPS[1:]
                self.wardrobe_app.tops_image_path = new_top_path_no_bg_renamed
                self.update_photo(new_top_path_no_bg_renamed, self.wardrobe_app.top_image_label)

                # Set autocomplete for top entry after uploading
                self.set_autocomplete(self.top_name_entry, self.wardrobe_app.all_tops_list)

    def upload_bottom(self):
        new_bottom_path = self.upload_image(self.wardrobe_app.BOTTOMS_FOLDER)
        if new_bottom_path:
            # Get details from the user
            bottom_name = WardrobeUI.AutocompleteEntryDialog(self.root, "Enter Bottom Name", "Enter the name for the bottom:", self.wardrobe_app.all_tops_list).result
            bottom_size = simpledialog.askstring("Input", "Enter the size for the bottom:")
            bottom_color = simpledialog.askstring("Input", "Enter the color for the bottom:")
            bottom_brand = simpledialog.askstring("Input", "Enter the brand for the bottom:")
            bottom_genre = simpledialog.askstring("Input", "Enter the genre for the bottom:")
            bottom_fabric = simpledialog.askstring("Input", "Enter the fabric for the bottom:")

            # Remove the background from the uploaded bottom image
            new_bottom_path_no_bg = self.remove_background(new_bottom_path)

            if new_bottom_path_no_bg:
                # Rename the uploaded bottom image with the user-provided name
                new_bottom_path_no_bg_renamed = os.path.join(self.wardrobe_app.BOTTOMS_FOLDER, f"{bottom_name}.png")
                os.rename(new_bottom_path_no_bg, new_bottom_path_no_bg_renamed)

                # Store details in the SQLite database
                self.wardrobe_app.store_clothing_details(bottom_name, "bottom", bottom_size, bottom_color, bottom_brand, bottom_genre, bottom_fabric)

                self.wardrobe_app.bottom_images = [new_bottom_path_no_bg_renamed] + self.wardrobe_app.ALL_BOTTOMS[1:]
                self.wardrobe_app.bottom_image_path = new_bottom_path_no_bg_renamed
                self.update_photo(new_bottom_path_no_bg_renamed, self.wardrobe_app.bottom_image_label)

                # Set autocomplete for bottom entry after uploading
                self.set_autocomplete(self.bottom_name_entry, self.wardrobe_app.all_bottoms_list)

  
if __name__ == '__main__':
    root = tk.Tk()
    db_handler = DatabaseHandler("wardrobe_database.db")
    app = WardrobeApp(root, db_handler=None)
    ui = WardrobeUI(root, app)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


