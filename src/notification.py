import customtkinter as ctk
from random import uniform
import pywinstyles

from properties import COLOR

class Notification(ctk.CTkLabel):
    def __init__(self, master, text: str, duration: float):
        super().__init__(master, fg_color=COLOR.TRANSPARENT,
                        text=text, text_color=COLOR.BAD,
                        font=ctk.CTkFont('Source Code Pro', 24))
        self.duration = duration
        self.duration_ = duration
        self.random_position = uniform(0.2, 0.8)
        self.random_end_pos = uniform(0.1, 0.9)
        self.place(x=-100, y=-100)
        pywinstyles.set_opacity(self, value=0.5, color='#000001')
        self.master.after(21, lambda: self.place_animate(0))

    def place_animate(self, position) -> None:
        if self.duration <= 0:
            self.master.after(21, self.destroy_animate)
            return
        self.place(relx=self.random_position, y=position, anchor=ctk.CENTER)
        self.master.after(21, lambda: self.place_animate(position + 1 + self.random_end_pos))
        self.duration -= .1

    def destroy_animate(self) -> None:
        if self.duration >= 0.5:
            self.destroy()
            return
        pywinstyles.set_opacity(self, value=0.5 - float(self.duration), color='#000001')
        self.after(31, self.destroy_animate)
        self.duration += .05
