from collections.abc import Callable

from tkinter import Button, PhotoImage
from customtkinter import CTkButton, CTkImage
from PIL import Image

from PhoneBook import shared
from PhoneBook.utils.widget_utils.messagebox_util import MyMessagebox
from PhoneBook.utils.sound_utils import click_sound, close_sound



def track_clicks(command: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        shared.click_count += 1
        if shared.click_count == 100:
            shared.root.after(100, lambda: MyMessagebox(420).message("تبریک! تو تا الان روی ۱۰۰ تا دکمه‌های این برنامه !کلیک کردی", "😍 عه! چه جالب", "!دستاورد باز شد"))
        result = command(*args, **kwargs) if command else None
        return result
    return wrapper


def my_button(window, x, y, text=None, image=None, command=None, bg="#0D1729", fg="white", font="Vazir", size=12, style="normal", cursor="hand2", width=None, height=None, use_close_sound=False, **kwargs) -> Button:
    button = Button(window, text=text, image=image, command=track_clicks(command), bg=bg, fg=fg, font=(font, size, style), cursor=cursor, width=width, height=height, **kwargs)
    button.place(x=x, y=y)

    if not use_close_sound:
        button.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() else None)
    else:
        button.bind("<Button-1>", lambda event: close_sound() if shared.sound.get() else None)

    return button


def my_button_ctk(window, x, y, text=None, image=None, width=110, height=50, corner_radius=10, fg_color="#0D1729", hover_color="#3c3c3c", text_color="white", border_color="#009300", font="Vazir", size=12, command=None) -> CTkButton:
    button = CTkButton(window, text=text, image=image, command=track_clicks(command), width=width, height=height, border_width=1, border_color=border_color if text != "لغو" else "#C94A4A", corner_radius=corner_radius, fg_color=fg_color, hover_color=hover_color, text_color=text_color, font=(font, size))
    button.place(x=x, y=y)

    button.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() else None)

    return button


def button_image(window, address, x, y, width, height, bg="#0D1729", activebackground="#0D1729", color_change=False, color1="#3c3c3c", color2="#373535", use_close_sound=False, command=None) -> Button:
    image = PhotoImage(file=address)

    button = my_button(window=window, image=image, x=x, y=y,bg=bg, width=width, height=height, activebackground=activebackground, relief="flat", bd=0, use_close_sound=use_close_sound, command=command)
    button.image = image

    if color_change:
        button.bind("<Enter>", lambda event: button.config(bg=color1))
        button.bind("<Leave>", lambda event: button.config(bg=color2))

    return button


def button_image_ctk(window, address, x, y, width, height, bg_color="#112034", hover_color="#16243A", command=None) -> CTkButton:
    image = CTkImage(light_image=Image.open(address), dark_image=Image.open(address), size=(width, height))

    button = CTkButton(window, image=image, text="", width=160, height=58, corner_radius=10, border_color="#26364A", border_width=1, fg_color=bg_color, hover_color=hover_color, anchor="w", command=track_clicks(command))
    button.place(x=x, y=y)

    button.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() else None)

    button.image = image

    return button

def toggle_button(boolean_var, name_button, name_image1, name_image2) -> None:
    if not boolean_var.get():
        if name_button == shared.pin_btn:
            shared.root.attributes("-topmost", True)
        boolean_var.set(True)
        name_button.config(image=name_image1)
        name_button.image = name_image1

    else:
        if name_button == shared.pin_btn:
            shared.root.attributes("-topmost", False)
        boolean_var.set(False)
        name_button.config(image=name_image2)
        name_button.image = name_image2
