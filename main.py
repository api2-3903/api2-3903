# main.py
import tkinter as tk
from wardrobe_app import WardrobeApp
from database_handler import DatabaseHandler

if __name__ == '__main__':
    root = tk.Tk()
    db_handler = DatabaseHandler("wardrobe_database.db")
    app = WardrobeApp(root, db_handler)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
