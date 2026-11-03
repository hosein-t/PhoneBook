from customtkinter import CTkFrame
from tkinter import Widget
from PhoneBook.utils.widget_utils.label_utils import label_image
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.path_utils import get_asset
from PhoneBook.utils.text_util import shorten_text



class SearchContact:
    def __init__(
            self,
            name: str,
            number: str,
            group: str,
            parent: Widget,
            avatars_path: str
        ):

        self.name = name
        self.number = number
        self.group = group
        self.window = parent
        self.avatars_path = avatars_path

        self.frame = CTkFrame(self.window, height=70, corner_radius=15, fg_color="#142139", border_width=1, border_color="#2b3545")
        self.frame.pack(fill="x", padx=(0, 15), pady=5)

        self.create_widgets()

    def create_widgets(self):
        label_image(self.frame, address=self.avatars_path, x=550, y=7, bg="#152238")
        display_name = shorten_text(self.name, max_width=130, font_name="Vazir", size=13)
        my_label(self.frame, x=537, y=34, text=display_name, bg="#142139", anchor=True, size=13)

        label_image(self.frame, x=220, y=23, address=get_asset(r"contacts\phone_label.svg"), bg="#152238")
        my_label(self.frame, text=self.number, x=253, y=22, bg="#152238", size=13)

        label_image(self.frame, x=15, y=22, address=get_asset(r"contacts\group_label.svg"), bg="#152238")
        display_group = shorten_text(self.group, max_width=155, font_name="Vazir", size=13)
        my_label(self.frame, text=display_group, x=50, y=22, bg="#152238", size=12)
