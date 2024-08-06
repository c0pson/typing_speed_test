from wonderwords import RandomSentence
import customtkinter as ctk
import pywinstyles
import string
import time

from properties import COLOR
from notification import Notification

class TypingTest(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color=COLOR.TRANSPARENT)
        self.sentence_gen = RandomSentence()
        self.sentence: str = self.get_sentence()
        self.valid_input: list[str] = list( string.ascii_lowercase + 
                                            string.ascii_uppercase +
                                            string.digits + '.,-\'` ')
        self.char_labels: list[ctk.CTkLabel] = []
        self.user_inputs: list[ctk.CTkLabel] = []
        self.current_char_index: int = 0
        self.font = ctk.CTkFont('Source Code Pro', size=35)
        self.cancel: bool = False
        self.bad_chars: int = 0
        self.penalty: float = 0.5
        self.sentence_frame = ctk.CTkFrame(self, fg_color=COLOR.TRANSPARENT)
        self.sentence_frame.pack(padx=5, pady=5, side=ctk.TOP, fill=ctk.X, expand=True)
        self.display_sentence()
        self.user_input_frame = ctk.CTkFrame(self, fg_color=COLOR.TRANSPARENT)
        self.user_input_frame.pack(padx=5, pady=5, side=ctk.TOP, fill=ctk.X, expand=True)
        self.master.bind('<KeyPress>', self.on_press)
        self.master.bind('<KeyRelease>', self.on_release)
        self.update_height()
        pywinstyles.set_opacity(self.sentence_frame, value=0.99, color='#000001')
        pywinstyles.set_opacity(self.user_input_frame, value=0.99, color='#000001')

    def on_press(self, event) -> None:
        if self.current_char_index == 0 and event.char in self.valid_input:
            self.cancel = False
            self.start_timer()
        if len(self.sentence) == self.current_char_index and event.keysym != 'BackSpace':
            return
        char: str = event.char
        if char in self.valid_input:
            if self.char_labels[self.current_char_index].cget('text') == char:
                self.char_labels[self.current_char_index].configure(text_color=COLOR.GOOD)
            else:
                Notification(self.master, f'-{self.penalty}', 2)
                self.char_labels[self.current_char_index].configure(text_color=COLOR.BAD)
                self.start_time -= self.penalty
                self.bad_chars += 1
                if not self.bad_chars % 10:
                    self.penalty += .5 
            self.current_char_index += 1
            self.create_char_label(char=char, frame=self.user_input_frame)
        elif event.keysym == 'BackSpace':
            if self.current_char_index == 0:
                return
            self.current_char_index -= 1
            self.user_inputs[self.current_char_index].destroy()
            self.user_inputs.pop(self.current_char_index)
            self.char_labels[self.current_char_index].configure(text_color=COLOR.TEXT)

    def on_release(self, event) -> None:
        if self.current_char_index != len(self.sentence):
            return
        if event.keysym == 'Return':
            self.end_timer()
            self.restart()

    def get_sentence(self) -> str:
        return self.sentence_gen.sentence()

    def display_sentence(self) -> None:
        for char in self.sentence:
            self.create_char_label(char, self.sentence_frame)

    def create_char_label(self, char: str, frame: ctk.CTkFrame) -> None:
        char_label = ctk.CTkLabel(frame, text=char, font=self.font, corner_radius=3, fg_color=COLOR.BACKGROUND,
                                text_color=COLOR.TEXT if frame is self.sentence_frame else COLOR.GRAY,)
        char_label.pack(side=ctk.LEFT, padx=2, pady=2)
        if frame is self.sentence_frame:
            self.char_labels.append(char_label)
        elif frame is self.user_input_frame:
            self.user_inputs.append(char_label)

    def update_font(self) -> None:
        if not self.current_char_index:
            self.update_height()
        for child in self.master.winfo_children():
            if isinstance(child, ctk.CTkLabel) and not isinstance(child, Notification):
                child.configure(font=self.font)

    def update_height(self) -> None:
        self.create_char_label(' ', self.user_input_frame)
        self.after(201, lambda: self.user_inputs[0].destroy())
        self.after(221, lambda: self.user_inputs.pop(0))

    def restart(self) -> None:
        self.accuracy()
        self.cancel = True
        self.bad_chars = 0
        self.penalty = .5
        self.master.unbind('<KeyPress>')
        self.master.unbind('<KeyRelease>')
        self.animate_hide(val=0)

    def start_timer(self) -> None:
        self.start_time = time.time()
        self.continue_timer()

    def continue_timer(self) -> None:
        if self.cancel:
            return
        self.end_time: float = round(time.time() - self.start_time, 2)
        self.master.update_timer()
        self.master.after(50, self.continue_timer)

    def end_timer(self) -> None:
        self.cancel = True
        self.end_time = round(time.time() - self.start_time, 2)
        self.master.update_timer()
        wpm = len(self.sentence.split()) / (self.end_time / 60)
        cpm = len(self.sentence) / (self.end_time / 60)
        self.master.update_counter(wpm, cpm)
        accuracy_ = int((1-(self.bad_chars/len(self.sentence)))*100)
        self.master.insert_to_db(wpm, cpm, accuracy_)

    def animate_hide(self, val: float) -> None:
        if val >= .9:
            for child in self.sentence_frame.winfo_children():
                child.destroy()
            for child in self.user_input_frame.winfo_children():
                child.destroy()
        if val >= .99:
            self.sentence = self.sentence_gen.sentence()
            self.current_char_index = 0
            self.char_labels = []
            self.user_inputs = []
            self.display_sentence()
            self.update_height()
            self.master.bind('<KeyPress>', self.on_press)
            self.master.bind('<KeyRelease>', self.on_release)
            self.animate_show(val=0)
            return
        pywinstyles.set_opacity(self, value=(0.9-val), color='#000001')
        self.master.after(16, lambda: self.animate_hide(val=val+0.03))

    def animate_show(self, val: float) -> None:
        if val >= .99:
            return
        pywinstyles.set_opacity(self, value=(0+val), color='#000001')
        self.master.after(16, lambda: self.animate_show(val=val+0.03))

    def accuracy(self) -> None:
        self.master.update_percentage(int((1-(self.bad_chars/len(self.sentence)))*100))
