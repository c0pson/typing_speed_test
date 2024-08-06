from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib.figure import Figure

import customtkinter as ctk
from PIL import Image
import pywinstyles

from tools import resource_path
from properties import COLOR
import user_statistics

class Menu(ctk.CTkFrame):
    def __init__(self, master, type_test) -> None:
        super().__init__(master, fg_color=COLOR.TRANSPARENT)
        self.type_test = type_test
        self.font = ctk.CTkFont('Source Code Pro', 25)
        self.show_statistics()
        self.create_time_label()
        self.create_resize_buttons()
        self.down_menu = ctk.CTkFrame(master, fg_color=COLOR.TRANSPARENT)
        self.down_menu.pack(side=ctk.BOTTOM, padx=20, pady=20, fill=ctk.X)
        self.create_wpm_cpm()
        self.accuracy_label()
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

    def accuracy_label(self) -> None:
        self.accuracy = ctk.CTkLabel(self.down_menu, text='-',
                                    font=self.font)
        self.accuracy.pack(side=ctk.LEFT, anchor=ctk.CENTER, expand=True)

    def update_accuracy(self, accuracy: int) -> None:
        self.accuracy.configure(text=f'{accuracy}%')

    def show_statistics(self) -> None:
        stats_icon = Image.open(resource_path('assets\\stats.png')).resize((32, 32))
        stats_image = ctk.CTkImage(light_image=stats_icon, dark_image=stats_icon, size=(32, 32))
        self.show_statistics_button = ctk.CTkLabel(self, text='', image=stats_image)
        self.show_statistics_button.pack(side=ctk.LEFT, padx=10, pady=10)
        self.show_statistics_button.bind('<Button-1>', self.display_statistics)

    def display_statistics(self, event) -> None:
        stats = user_statistics.get_stats()
        times = list(range(len(stats)))
        wpm_values = [stat[1] for stat in stats]
        wpm_values = list(reversed(wpm_values))
        accuracy_values = [stat[3] for stat in stats]
        accuracy_values = list(reversed(accuracy_values))
        fig = Figure(figsize=(6, 4), dpi=100)
        fig.patch.set_facecolor(COLOR.BACKGROUND)
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLOR.BACKGROUND)
        ax.plot(times, wpm_values, label="WPM", marker='o')
        ax.plot(times, accuracy_values, label="Accuracy", marker='o')
        ax.legend(frameon=False, fontsize=10, loc='best', labelcolor=COLOR.TEXT)
        ax.tick_params(axis='x', colors=COLOR.TEXT)
        ax.tick_params(axis='y', colors=COLOR.TEXT)
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(10))
        ax.xaxis.set_minor_locator(AutoMinorLocator(4))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.grid(which='major', linestyle='-', linewidth='0.5', color=COLOR.GRAY)
        ax.grid(which='minor', linestyle='-', linewidth='0.5', color=COLOR.GRAY)
        for spine in ax.spines.values():
            spine.set_edgecolor(COLOR.TEXT)
        self.chart_frame = ctk.CTkFrame(self.master, fg_color=COLOR.BACKGROUND)
        self.chart_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER, relwidth=1, relheight=1)
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)
        self.master.bind('<Escape>', self.close_statistics)

    def close_statistics(self, event) -> None:
        self.chart_frame.destroy()
        self.master.unbind('<Escape>')
