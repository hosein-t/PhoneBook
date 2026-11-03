from customtkinter import CTkLabel
from tkinter import Frame, Canvas

from PhoneBook import shared
from PhoneBook.utils.path_utils import CONTACTS_FILE
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.widget_utils.scrollbar_util import MyScrollbar
from PhoneBook.utils.json_utils import read_json
from PhoneBook.models.contact import Contact, enable_mouse_scroll



class FavoritesView:
    def __init__(self, menu):
        self.menu = menu

        self.favorite_frame = None
        self.favorites_scrollbar = None
        self.favorites_frame = None
        self.favorites_canvas = None

        self.prepare_menu()
        self.create_favorites_frame()
        self.create_favorites_canvas()
        self.add_contact_to_favorites_frame()

    def prepare_menu(self):
        self.menu.add_contact_btn.place_forget()
        self.menu.add_group_btn.place_forget()
        self.menu.changing_button_colors("favorites_btn")
        self.menu.clear_frames()
        self.menu.hide_search_canvas()
        self.menu.reset_error_widgets()

    def create_favorites_frame(self):
        self.favorites_frame = Frame(shared.root, bg="#0D1729", width=660, height=475)
        self.favorites_frame.place(x=230, y=90)
        shared.active_frames.append(self.favorites_frame)

    def create_favorites_canvas(self):
        self.favorites_canvas = Canvas(self.favorites_frame, bg="#0D1729", highlightthickness=0)
        self.favorites_canvas.place(x=0, y=40, width=660, height=435)

        self.favorites_scrollbar = MyScrollbar(self.favorites_frame, self.favorites_canvas, height=441)

        self.favorite_frame = Frame(self.favorites_canvas, bg="#0D1729")
        self.favorites_canvas.create_window((0, 0), window=self.favorite_frame, anchor="nw", width=630)
        self.favorites_canvas.configure(yscrollcommand=self.favorites_scrollbar.scrollbar.set)

        self.favorite_frame.bind("<Configure>", self.on_frame_configure)
        enable_mouse_scroll(self.favorite_frame, self.scroll_favorites)

    def on_frame_configure(self, _):
        self.favorites_canvas.configure(scrollregion=self.favorites_canvas.bbox("all"))

        if len(self.favorite_frame.winfo_children()) <= 5:
            self.favorites_scrollbar.scrollbar.place_forget()
        else:
            self.favorites_scrollbar.scrollbar.place(x=630, y=35)

    def scroll_favorites(self, event):
        if len(self.favorite_frame.winfo_children()) > 5:
            self.favorites_canvas.yview_scroll(int(-event.delta / 120), "units")

    def add_contact_to_favorites_frame(self):
        contacts_data = read_json(CONTACTS_FILE)

        favorites_count = sum(1 for contact in contacts_data if contact.get("favorite", False))
        favorite_count_text = my_label(self.favorites_frame, text=":تعداد علاقه‌مندی‌ها", x=48, y=-3, size=11, fg="#AAB7CC", font="Samim WOL")

        shared.favorite_count_label = CTkLabel(self.favorites_frame, text=favorites_count, width=38, height=24, fg_color="#292342", text_color="#D0C4FF", font=("TkFixedFont", 14, "bold"), corner_radius=12, border_width=1, border_color="#62558F")
        shared.favorite_count_label.place(x=4, y=0)

        if favorites_count == 0:
            shared.favorite_count_label.place_forget()
            favorite_count_text.place_forget()

        if contacts_data:
            has_favorite = False

            for contact in contacts_data:
                if contact.get("favorite", False):
                    Contact(contact["name"], contact["number"], contact["group"], contact.get("favorite", False), self.favorite_frame, favorites_only=True)
                    has_favorite = True

            if not has_favorite:
                shared.L3 = my_label(self.favorites_frame, text="!مخاطبی به علاقه‌مندی‌ها اضافه نشده است", x=100, y=150, bg="#0D1729", fg="#7DD3FC", size=18, font="Samim WOL")
                shared.L4 = my_label(self.favorites_frame, text=".برای افزودن مخاطب به علاقه‌مندی‌ها، روی آیکون ستاره‌ی کنار هر مخاطب کلیک کنید", x=60, y=200, bg="#0D1729", fg="gray", size=11, font="Samim WOL")
        else:
            shared.L3 = my_label(self.favorites_frame, text="!مخاطبی به علاقه‌مندی‌ها اضافه نشده است", x=100, y=150, bg="#0D1729", fg="#7DD3FC", size=18, font="Samim WOL")
            shared.L4 = my_label(self.favorites_frame, text=".برای افزودن مخاطب به علاقه‌مندی‌ها، روی آیکون ستاره‌ی کنار هر مخاطب کلیک کنید", x=60, y=200, bg="#0D1729", fg="gray", size=11, font="Samim WOL")