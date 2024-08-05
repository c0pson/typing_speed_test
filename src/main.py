import customtkinter as ctk

from typing_test import TypingTest
from tools import resource_path
from menu import Menu

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.load_font()
        self.title('Type speed')
        self.iconbitmap(resource_path('assets\\icon.ico'))
        self.type_test = TypingTest(self)
        self.menu = Menu(self, self.type_test)
        self.type_test.pack(padx=20, pady=20, expand=True)
        self.after(201, lambda: self.state('zoomed'))

    def load_font(self) -> None:
        ctk.FontManager.windows_load_font(resource_path('fonts\\SourceCodePro.ttf'))

    def update_timer(self) -> None:
        self.menu.update_timer(time=self.type_test.end_time)

    def update_counter(self, wpm: float, cpm: float) -> None:
        self.menu.update_wpm_cpm(wpm, cpm)

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
