import tkinter as tk

root = tk.Tk()


class Settings:
    """Параметры игры"""

    def __init__(self):
        self.admin_width = 1536
        self.admin_height = 864
        self.width = 1536
        self.height = 864
        self.fps = 120
        self.speed_x = 153
        self.speed_y = 86
