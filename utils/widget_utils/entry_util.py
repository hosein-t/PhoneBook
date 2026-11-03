from customtkinter import CTkEntry
from PhoneBook import shared
from PhoneBook.utils.sound_utils import click_sound



def my_entry_ctk(window, x=0, y=0, width=None, height=None, font="Vazir", size=18, style="normal", bd=1, justify="right", placeholder_text=None, **kwargs) -> CTkEntry:
    def count_entry_click(_):
        shared.click_count += 1

    def spelling_correction(char, new_char):
        if entry.get().endswith(char):
            text_search = entry.get()[:-1] + new_char
            entry.delete(0, "end")
            entry.insert(0, text_search)

    entry = CTkEntry(window, width=width, height=height, placeholder_text=placeholder_text, fg_color="#101C31", text_color="#F7F7F7", font=(font, size, style), border_width=1 if bd != 0 else 0, border_color="#30415A", corner_radius=6, justify=justify, **kwargs)
    entry.place(x=x, y=y)

    entry.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() else None)
    entry.bind("<Button-1>", count_entry_click, add="+")
    entry.bind("<FocusIn>", lambda event: entry.configure(border_color="#0078D4"))
    entry.bind("<FocusOut>", lambda event: entry.configure(border_color="#30415A"))
    entry.bind("<KeyRelease>", lambda event: spelling_correction("ي", "ی"))

    return entry