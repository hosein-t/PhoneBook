from customtkinter import CTkFrame
from tkinter import PhotoImage
from PhoneBook.utils.path_utils import get_asset
from PhoneBook.utils.widget_utils.button_utils import my_button
from PhoneBook.utils.widget_utils.label_utils import label_image



class BaseCard:
    def __init__(self, name, parent, avatars_path):
        self.name = name
        self.window = parent

        self.frame = CTkFrame(parent, height=70, corner_radius=15, fg_color="#142139", border_width=1, border_color="#2b3545")
        self.frame.pack(fill="x", padx=(0, 15), pady=5)

        self.trash_img = PhotoImage(file=get_asset(r"contacts\trash_button.svg"))
        self.trash_img2 = PhotoImage(file=get_asset(r"contacts\trash_button2.svg"))

        self.edit_img = PhotoImage(file=get_asset(r"contacts\edit_button.svg"))
        self.edit_img2 = PhotoImage(file=get_asset(r"contacts\edit_button2.svg"))

        label_image(self.frame, address=avatars_path, x=550, y=7, bg="#152238")

    def create_buttons(self, command_trash_btn, command_edit_btn):
        self.TRASH_button = my_button(self.frame, image=self.trash_img, x=15, y=22, bg="#152238", width=24, height=24, activebackground="#152238", bd=0, command=command_trash_btn)
        self.EDIT_button = my_button(self.frame, image=self.edit_img, x=55, y=24, bg="#152238", width=22, height=22, bd=0, activebackground="#152238", command=command_edit_btn)

        self.TRASH_button.bind("<Enter>", lambda event: self.TRASH_button.config(image=self.trash_img2))
        self.TRASH_button.bind("<Leave>", lambda event: self.TRASH_button.config(image=self.trash_img))

        self.EDIT_button.bind("<Enter>", lambda event: self.EDIT_button.config(image=self.edit_img2))
        self.EDIT_button.bind("<Leave>", lambda event: self.EDIT_button.config(image=self.edit_img))