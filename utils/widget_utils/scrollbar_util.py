from customtkinter import CTkScrollbar
from PhoneBook import shared
from PhoneBook.utils.sound_utils import click_sound



class MyScrollbar:
    def __init__(self, window, canvas, x=860, y=125 , width=13, height=444):
        self.scrollbar = CTkScrollbar(window, width=width, height=height, fg_color="#0D1729", button_color="#3c3c3c", button_hover_color="#4a4a4a", corner_radius=6, command=canvas.yview)
        self.scrollbar.place(x=x, y=y)

        self.scrollbar_dragging = False

        self.scrollbar.bind("<Button-1>", self.start_drag)
        self.scrollbar.bind("<ButtonRelease-1>", self.stop_drag)
        self.scrollbar.bind("<Enter>", self.on_enter)
        self.scrollbar.bind("<Leave>", self.on_leave)

    def start_drag(self, _):
        self.scrollbar_dragging = True
        self.scrollbar.configure(width=15)
        click_sound() if shared.sound.get() else None
        shared.click_count += 1

    def stop_drag(self, _):
        self.scrollbar_dragging = False
        self.scrollbar.configure(width=13, fg_color="#1A2536")

    def on_enter(self, _):
        self.scrollbar.configure(cursor="sb_v_double_arrow", width=15, corner_radius=3, fg_color="#1A2536")

    def on_leave(self, _):
        if not self.scrollbar_dragging:
            self.scrollbar.configure(cursor="arrow", width=13, corner_radius=6, fg_color="#0D1729")
