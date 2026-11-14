from tkinter import Frame
from PhoneBook import shared
from PhoneBook.utils.path_utils import get_asset
from PhoneBook.utils.widget_utils.button_utils import my_button_ctk
from PhoneBook.utils.widget_utils.label_utils import my_label, label_image



class LoginView:
    def __init__(self):
        self.frame = Frame(shared.root, width=898, height=598, background="#0D1729")
        self.frame.place(x=1, y=1)
        self.create_widgets()

    def create_widgets(self):
        label_image(self.frame, get_asset(r"login\background.png"), x=1, y=1)
        my_label(self.frame, text="!خوش اومدی", x=335, y=320, size=32, bg="#001335", fg="#f8f8f9", font="Samim WOL")
        my_label(self.frame, text="اولین دفترچه تلفن فارسی زبان ویندوز", x=270, y=390, size=18, bg="#001335", fg="#4db6f8", font="Samim WOL")
        my_label(self.frame, text="نسخه 1.1.2", x=410, y=534, size=12, bg="#03142d", fg="#8AB4F8")
        my_button_ctk(self.frame, x=336, y=460, text="▶ شروع کنیم", border_color="#4B91F5", fg_color="#176DE0", hover_color="#2175E2", width=230, height=60, size=24, font="Samim WOL", command=self.destroy_frame)

    def destroy_frame(self):
        self.frame.destroy()
        shared.registered = True
