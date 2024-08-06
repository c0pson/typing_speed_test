from ctypes import windll, byref, sizeof, c_int
import customtkinter as ctk

from typing_test import TypingTest
from tools import resource_path
from properties import COLOR
import user_statistics
from menu import Menu

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=COLOR.BACKGROUND)
        self.load_font()
        self.title('Type speed')
        self.iconbitmap(resource_path('assets\\icon.ico'))
        user_statistics.setup_database()
        self.type_test = TypingTest(self)
        self.menu = Menu(self, self.type_test)
        self.type_test.pack(padx=20, pady=20, expand=True)
        self.toggle_fullscreen()

    def load_font(self) -> None:
        ctk.FontManager.windows_load_font(resource_path('fonts\\SourceCodePro.ttf'))

    def update_timer(self) -> None:
        self.menu.update_timer(time=self.type_test.end_time)

    def update_counter(self, wpm: float, cpm: float) -> None:
        self.menu.update_wpm_cpm(wpm, cpm)

    def update_percentage(self, accuracy: int) -> None:
        self.menu.update_accuracy(accuracy)

    def insert_to_db(self, wpm: float, cpm: float, accuracy: int) -> None:
        user_statistics.insert_stat(wpm, cpm, accuracy)

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', True)
        self.unbind('<F11>')
        self.bind('<F11>', self.exit_fullscreen)
        self.change_title_bar_color()

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)
        self.unbind('<F11>')
        self.bind('<F11>', self.toggle_fullscreen)
        self.change_title_bar_color()

    def change_title_bar_color(self):
        HWND = windll.user32.GetParent(self.winfo_id())
        DWMWA_ATTRIBUTE = 35
        COLOR = 0x00442F35 # 0x00bbggrr | 352F44
        windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
