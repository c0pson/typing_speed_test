import customtkinter as ctk
import pywinstyles

from properties import COLOR

class Menu(ctk.CTkFrame):
    def __init__(self, master, type_test) -> None:
        super().__init__(master, fg_color=COLOR.TRANSPARENT)
        self.type_test = type_test
        self.font = ctk.CTkFont('Source Code Pro', 25)
        self.create_time_label()
        self.create_resize_buttons()
        self.down_menu = ctk.CTkFrame(master, fg_color=COLOR.TRANSPARENT)
        self.down_menu.pack(side=ctk.BOTTOM, padx=20, pady=20, fill=ctk.X)
        self.create_wpm_cpm()
        self.pack(side=ctk.TOP, fill=ctk.X)
        pywinstyles.set_opacity(self, value=0.7, color='#ffffff')
        pywinstyles.set_opacity(self.down_menu, value=0.7, color='#ffffff')

    def create_resize_buttons(self) -> None:
        self.plus_button = ctk.CTkButton(self, text="+", command=self.on_plus,
                                        width=20, height=20, hover=False,
                                        font=self.font, fg_color=COLOR.TRANSPARENT,
                                        text_color=COLOR.TEXT)
        self.plus_button.pack(side=ctk.RIGHT, padx=5, pady=5)
        self.minus_button = ctk.CTkButton(self, text="-", command=self.on_minus,
                                        width=20, height=20, hover=False,
                                        font=self.font, fg_color=COLOR.TRANSPARENT,
                                        text_color=COLOR.TEXT)
        self.minus_button.pack(side=ctk.RIGHT, padx=5, pady=5)

    def on_plus(self) -> None:
        current_size = self.type_test.font.cget('size')
        self.type_test.font.configure(size=(current_size + 2))
        self.type_test.update_font()

    def on_minus(self) -> None:
        current_size = self.type_test.font.cget('size')
        self.type_test.font.configure(size=(current_size - 2))
        self.type_test.update_font()

    def create_time_label(self) -> None:
        self.time_label = ctk.CTkLabel(self, text='-', text_color=COLOR.TEXT,
                                        font=self.font)
        self.time_label.pack(side=ctk.LEFT, padx=5, pady=5)

    def update_timer(self, time: float) -> None:
        time_ = str(time)
        new_time = time_.split('.')
        self.time_label.configure(text=f'{new_time[0].zfill(2)}:{new_time[1].zfill(2)}')

    def create_wpm_cpm(self) -> None:
        self.words_per_minute = ctk.CTkLabel(self.down_menu, text='-',
                                            font=self.font)
        self.words_per_minute.pack(side=ctk.LEFT)
        self.characters_per_minute = ctk.CTkLabel(self.down_menu, text='-',
                                                font=self.font)
        self.characters_per_minute.pack(side=ctk.RIGHT)

    def update_wpm_cpm(self, wpm: float, cpm: float) -> None:
        self.words_per_minute.configure(text=round(wpm, 2))
        self.characters_per_minute.configure(text=round(cpm, 2))
