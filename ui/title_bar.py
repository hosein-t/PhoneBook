from random import choice

from tkinter import Frame, Button, PhotoImage, Canvas, Misc
from customtkinter import CTkFrame, CTkEntry

from PhoneBook import shared
from PhoneBook.models.contact import avatars
from PhoneBook.models.search_contact import SearchContact
from PhoneBook.utils.path_utils import get_asset, CONTACTS_FILE
from PhoneBook.utils.widget_utils.button_utils import button_image, toggle_button
from PhoneBook.utils.widget_utils.label_utils import my_label, label_image
from PhoneBook.utils.widget_utils.tooltip_util import tooltip
from PhoneBook.utils.widget_utils.messagebox_util import MyMessagebox
from PhoneBook.utils.sound_utils import click_sound
from PhoneBook.utils.json_utils import read_json
from PhoneBook.ui.button_commands import close_tab



x, y = 0, 0

def start_move(event):
    global x, y
    x = event.x_root - shared.root.winfo_x()
    y = event.y_root - shared.root.winfo_y()

def move_window(event):
    shared.root.geometry(f"+{event.x_root - x}+{event.y_root - y}")


class CreateTitleBar:
    def __init__(self):
        self.title_bar = Frame(shared.root, bg="#0D1729", height=60, width=896)
        self.title_bar.place(x=1, y=1)
        self.title_bar.bind("<Button-1>", start_move)
        self.title_bar.bind("<B1-Motion>", move_window)

        self.search_box = None
        self.no_contact_img = None
        self.no_contact_label = None

        shared.search_canvas = Canvas(shared.root, bg="#0D1729", highlightthickness=0)
        self.search_frame = Frame(shared.search_canvas, bg="#0D1729", height=475)
        shared.search_canvas.create_window((0, 0), window=self.search_frame, anchor="nw", width=630)
        self.search_frame.bind("<Configure>", lambda event: shared.search_canvas.configure(scrollregion=shared.search_canvas.bbox("all")))

        self.pin_img = PhotoImage(file=get_asset(r"title_bar\pin_button.svg"))
        self.unpin_img = PhotoImage(file=get_asset(r"title_bar\unpin_button.svg"))
        self.sound_img = PhotoImage(file=get_asset(r"title_bar\with_sound_button.svg"))
        self.silent_img = PhotoImage(file=get_asset(r"title_bar\silent_button.svg"))
        self.search_img = PhotoImage(file=get_asset(r"title_bar\search_button.svg"))
        self.search_img2 = PhotoImage(file=get_asset(r"title_bar\search_button2.svg"))
        
        self.create_search_box()
        self.create_buttons()

    def create_buttons(self):
        close_btn = button_image(self.title_bar, get_asset(r"title_bar\close_button.svg"), x=848, y=10, width=38, height=38, bg="#0D1729", command=close_tab, color_change=True, color1="#B03E3E", color2="#0D1729", use_close_sound=True)
        tooltip(close_btn, "بستن برنامه")

        shared.pin_btn = Button(self.title_bar, image=self.unpin_img if shared.pin.get() == False else self.pin_img, bg="#0D1729", activebackground="#0D1729", bd=0, relief="flat", cursor="hand2", command=lambda: toggle_button(shared.pin, shared.pin_btn, self.pin_img, self.unpin_img))
        shared.pin_btn.image = self.pin_img
        shared.pin_btn.place(x=808, y=10, width=40, height=40)
        shared.pin_btn.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() else None)
        shared.pin_btn.bind("<Button-1>", self.count_button_click, add="+")
        shared.pin_btn.bind("<Enter>", lambda event: shared.pin_btn.config(bg="#3c3c3c"))
        shared.pin_btn.bind("<Leave>", lambda event: shared.pin_btn.config(bg="#0D1729"))
        tooltip(shared.pin_btn, "سنجاق کردن/برداشتن سنجاق پنجره")

        sound_btn = Button(self.title_bar, image=self.sound_img if shared.sound.get() == True else self.silent_img, bg="#0D1729", activebackground="#0D1729", bd=0, relief="flat", cursor="hand2", command=lambda: toggle_button(shared.sound, sound_btn, self.sound_img, self.silent_img))
        sound_btn.image = self.sound_img
        sound_btn.place(x=768, y=10, width=40, height=40)
        sound_btn.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() else None)
        sound_btn.bind("<Button-1>", self.count_button_click, add="+")
        sound_btn.bind("<Enter>", lambda event: sound_btn.config(bg="#3c3c3c"))
        sound_btn.bind("<Leave>", lambda event: sound_btn.config(bg="#0D1729"))
        tooltip(sound_btn, "روشن/خاموش کردن صدای کلیک")

        recycle_bin_btn = button_image(self.title_bar, get_asset(r"title_bar\recycle_bin_button.svg"), x=728, y=10, width=38, height=38, bg="#0D1729", command=self.recycle_bin_command, color_change=True, color1="#3c3c3c", color2="#0D1729")
        tooltip(recycle_bin_btn, "سطل زباله")

    def create_search_box(self):
        search_frame = CTkFrame(self.title_bar, width=260, height=40, fg_color="#152238", border_color="#30415A", border_width=1, corner_radius=19)
        search_frame.place(x=350, y=17)

        Frame(search_frame, bg="#30415A", width=1, height=32).place(x=207, y=4)

        self.search_box = CTkEntry(search_frame, width=197, height=32, font=("Vazir", 15), placeholder_text="...جستجوی مخاطب", placeholder_text_color="#7F92AD", text_color="#DCE6F5", justify="right", fg_color="#152238", border_width=0, corner_radius=16)
        self.search_box.place(x=10, y=5)
        self.search_box.bind("<Button-1>", lambda event: click_sound() if shared.sound.get() and not self.search_box.get() else None)
        self.search_box.bind("<KeyRelease>", self.live_search_contacts)

        search_btn = button_image(search_frame, address=get_asset(r"title_bar\search_button.svg"), x=220, y=8, width=22, height=22, bg="#152238", activebackground="#152238", command=self.live_search_contacts)
        search_btn.bind("<Enter>", lambda event: search_btn.config(image=self.search_img2))
        search_btn.bind("<Leave>", lambda event: search_btn.config(image=self.search_img))

    def live_search_contacts(self, _=None):
        text_search = self.search_box.get()

        if self.no_contact_label is not None:
            self.no_contact_label.destroy()
            self.no_contact_label = None

        if self.no_contact_img is not None:
            self.no_contact_img.destroy()
            self.no_contact_img = None

        if text_search.endswith("ي"):
            text_search = text_search[:-1] + "ی"
            self.search_box.delete(0, "end")
            self.search_box.insert(0, text_search)

        if text_search:
            shared.search_canvas.place(x=230, y=90, width=660, height=475)
            Misc.tkraise(shared.search_canvas)

            for widget in self.search_frame.winfo_children():
                widget.destroy()

            contacts_data = read_json(CONTACTS_FILE)

            has_contact = False
            for contact in contacts_data:
                if contact["name"].startswith(text_search):
                    SearchContact(contact["name"], contact["number"], contact["group"], self.search_frame, choice(avatars))
                    has_contact = True

            if not has_contact:
                self.no_contact_img = label_image(shared.search_canvas, get_asset(r"title_bar\no_contacts_found.svg"), 235, 80)
                self.no_contact_label = my_label(shared.search_canvas, text="!مخاطبی پیدا نشد", x=215, y=230, fg="#7DD3FC", size=18, font="Samim WOL")

        else:
            shared.search_canvas.place_forget()

    @staticmethod
    def count_button_click(_):
        shared.click_count += 1

    @staticmethod
    def recycle_bin_command():
        MyMessagebox(420).message(".این قابلیت در نسخه‌های آینده اضافه خواهد شد ", "باشه", "🚧 به‌زودی")