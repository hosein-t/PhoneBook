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
        my_label(self.frame, text="نسخه 1.0", x=415, y=547, size=12, bg="#03142d", fg="#889cb8")
        my_button_ctk(self.frame, x=334, y=462, text="▶ شروع کنیم", border_color="#4B91F5", fg_color="#176DE0", hover_color="#2175E2", width=233, height=61, size=24, font="Samim WOL", command=self.destroy_frame)

    def destroy_frame(self):
        self.frame.destroy()
        shared.registered = True
