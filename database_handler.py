# database_handler.py
import sqlite3

class DatabaseHandler:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clothing_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                size TEXT,
                color TEXT,
                brand TEXT,
                genre TEXT,
                fabric TEXT
                path TEXT
            )
        ''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def store_clothing_details(self, name, clothing_type, size, color, brand, genre, fabric, path):
        try:
            self.cursor.execute('''
                INSERT INTO clothing_details (name, type, size, color, brand, genre, fabric, path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, clothing_type, size, color, brand, genre, fabric, path))
            self.conn.commit()
        except Exception as e:
            print(f"Error storing clothing details: {e}")


    def get_all_top_names(self):
        try:
            self.cursor.execute("SELECT name FROM clothing_details WHERE type='top'")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching top names: {e}")
            return []

    def get_all_bottom_names(self):
        try:
            self.cursor.execute("SELECT name FROM clothing_details WHERE type='bottom'")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching bottom names: {e}")
            return []
        

    #testing pending ....    #paths to be added
    def get_bottom_genre_by_path(self, path):
        try:
            self.cursor.execute("SELECT genre FROM clothing_details WHERE type='bottom' AND path=?", (path,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching bottom genre by path: {e}")
            return None

        
    def get_bottom_color_by_path(self, path):
        try:
            self.cursor.execute("SELECT color FROM clothing_details WHERE type='bottom' AND path=?", (path,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching bottom color by path: {e}")
            return None
        
    def get_top_genre_by_path(self, path):
        try:
            self.cursor.execute("SELECT genre FROM clothing_details WHERE type='top' AND path=?", (path,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching top genre by path: {e}")
            return None

        
    def get_top_color_by_path(self, path):
        try:
            self.cursor.execute("SELECT color FROM clothing_details WHERE type='top' AND path=?", (path,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching top color by path: {e}")
            return None