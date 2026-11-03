from PIL import Image, ImageTk, ImageGrab, ImageFilter
from collections.abc import Callable

from tkinter import Label
from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkImage, CTkButton

from PhoneBook import shared
from PhoneBook.utils.path_utils import get_asset
from PhoneBook.utils.sound_utils import messagebox_sound, click_sound



class MyMessagebox:
    def __init__(self, width: int = 400):
        overlay = self.create_blur_overlay()

        self.width = width

        self.transparent_color = None
        self.frame_top = None
        self.frame_message = None
        self.content_frame = None
        self.message_label = None
        self.icon_label = None
        self.button = None

        shared.click_count += 1

        self.messagebox = CTkToplevel(shared.root)
        self.messagebox.bind("<Destroy>", lambda event: overlay.destroy() if overlay is not None else None)

        self.toplevel_customization()

    def toplevel_customization(self):
        self.messagebox.update_idletasks()
        shared.root.update_idletasks()

        x = shared.root.winfo_rootx() + (shared.root.winfo_width() - self.width) // 2
        y = shared.root.winfo_rooty() + (shared.root.winfo_height() - 200) // 2

        self.messagebox.geometry(f"{self.width}x200+{x}+{y}")
        self.messagebox.resizable(False, False)
        self.messagebox.overrideredirect(True)
        self.messagebox.attributes("-topmost", True)
        self.messagebox.protocol("WM_DELETE_WINDOW", lambda: None)

        self.transparent_color = "#000001"
        self.messagebox.configure(fg_color=self.transparent_color)
        self.messagebox.attributes("-transparentcolor", self.transparent_color)

        self.frame_top = CTkFrame(self.messagebox, corner_radius=15, width=self.width, height=200, border_width=1, bg_color=self.transparent_color, fg_color="#202020", border_color="#0078d4")
        self.frame_top.grid(row=0, column=0, sticky="nsew")
        self.frame_top.grid_propagate(False)
        self.frame_top.grid_columnconfigure(0, weight=1)
        self.frame_top.grid_rowconfigure(1, weight=1)

        self.frame_message = CTkFrame(self.frame_top, fg_color="#272727", corner_radius=0, height=100, width=self.width - 2)
        self.frame_message.place(x=1, y=45)

    def message(self, message_text: str, button_text: str, title: str):
        self.create_title_label(title)
        self.create_text_label(message_text)
        self.create_icon_label(get_asset(r"icons_messagebox\info.png"))
        self.create_button(button_text, self.play_sound_click(self.messagebox.destroy), self.width - 105)
        messagebox_sound()
        self.messagebox.title(title)

    def question(self, question_text: str, title: str, yes_command: Callable):
        self.create_title_label(title)
        self.create_text_label(question_text)
        self.create_icon_label(get_asset(r"icons_messagebox\question.png"))
        self.create_button("خیر", self.play_sound_click(self.messagebox.destroy))

        def yes_btn_command():
            yes_command()
            self.messagebox.destroy()

        self.create_button("بله", self.play_sound_click(yes_btn_command), x=195)
        messagebox_sound()

        self.messagebox.title(title)

    def create_title_label(self, title: str):
        title_label = CTkLabel(self.frame_top, text=title, text_color="#FFFFFF", font=("Vazir", 14))
        title_label.place(x=15, y=10)

    def create_text_label(self, text: str):
        self.content_frame = CTkFrame(self.frame_message, fg_color="transparent")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.message_label = CTkLabel(self.content_frame, text=text, text_color="#FFFFFF", font=("Vazir", 15), wraplength=300, justify="left")
        self.message_label.pack(side="left", padx=(0, 10))

    def create_icon_label(self, icon_address: str):
        icon_image = CTkImage(light_image=Image.open(icon_address), dark_image=Image.open(icon_address), size=(48, 48))
        self.icon_label = CTkLabel(self.content_frame, text="", image=icon_image, fg_color="transparent")
        self.icon_label.image = icon_image
        self.icon_label.pack(side="left")

    def create_button(self, text: str, command: Callable, x: int = 295):
        self.button = CTkButton(self.frame_top, text=text, width=90, font=("Vazir", 14), height=31, hover_color="#0078d4", command=command)
        self.button.place(x=x, y=157)

    @staticmethod
    def play_sound_click(func):
        def wrapper(*args, **kwargs):
            if shared.sound.get():
                 click_sound()

            result = func(*args, **kwargs)

            return result
        return wrapper

    @staticmethod
    def create_blur_overlay():
        shared.root.update_idletasks()

        width = shared.root.winfo_width()
        height = shared.root.winfo_height()

        x, y = shared.root.winfo_rootx(), shared.root.winfo_rooty()

        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        blurred = screenshot.filter(ImageFilter.GaussianBlur(radius=3))

        dark_layer = Image.new("RGBA", blurred.size, (0, 0, 0, 50))
        blurred = Image.alpha_composite(blurred.convert("RGBA"), dark_layer)

        overlay_image = ImageTk.PhotoImage(blurred)

        overlay = Label(shared.root, image=overlay_image, borderwidth=0)
        overlay.image = overlay_image

        overlay.place(x=0, y=0, width=width, height=height)
        overlay.lift()

        return overlay
