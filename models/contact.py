from random import choice
from tkinter import Canvas, Widget, Frame, PhotoImage

from customtkinter import CTkComboBox

from PhoneBook import shared
from PhoneBook.models.base_card import BaseCard
from PhoneBook.utils.path_utils import get_asset, CONTACTS_FILE, GROUPS_FILE
from PhoneBook.utils.widget_utils.scrollbar_util import MyScrollbar
from PhoneBook.utils.widget_utils.button_utils import my_button, my_button_ctk
from PhoneBook.utils.text_util import shorten_text
from PhoneBook.utils.widget_utils.entry_util import my_entry_ctk
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.widget_utils.label_utils import label_image
from PhoneBook.utils.widget_utils.messagebox_util import MyMessagebox
from PhoneBook.utils.json_utils import read_json, write_json



def show_empty_contacts_message():
    shared.L1 = my_label(shared.root, text="!هیچ مخاطبی وجود ندارد", x=410, y=240, bg="#0D1729", fg="#7DD3FC", size=18, font="Samim WOL")
    shared.L2 = my_label(shared.root, text=".برای افزودن مخاطب جدید، روی گزینه «افزودن مخاطب» در سمت چپ صفحه کلیک کنید", x=280, y=290, bg="#0D1729", fg="gray", size=11, font="Samim WOL")

def hide_empty_contacts_message():
    if shared.L1:
        shared.L1.destroy()
        shared.L1 = None
    if shared.L2:
        shared.L2.destroy()
        shared.L2 = None

def on_frame_configure(_):
    contacts_canvas.configure(scrollregion=contacts_canvas.bbox("all"))
    if len(contacts_frame.winfo_children()) <= 5:
        scrollbar.scrollbar.place_forget()
    else:
        scrollbar.scrollbar.place(x=860, y=125)

def create_contacts_ui():
    global contacts_canvas, scrollbar, contacts_frame

    contacts_canvas = Canvas(shared.root, bg="#0D1729", highlightthickness=0)
    contacts_canvas.place(x=230, y=130, width=630, height=435)
    scrollbar = MyScrollbar(shared.root, contacts_canvas)

    contacts_frame = Frame(contacts_canvas, bg="#0D1729")
    contacts_canvas.create_window((0, 0), window=contacts_frame, anchor="nw", width=630)
    contacts_canvas.config(yscrollcommand=scrollbar.scrollbar.set)
    contacts_frame.bind("<Configure>", on_frame_configure)

    enable_mouse_scroll(contacts_frame)

def scroll_contacts(event):
    if len(contacts_frame.winfo_children()) > 5:
        contacts_canvas.yview_scroll(int(-event.delta / 120), "units")

def enable_mouse_scroll(widget, scroll_function=scroll_contacts):
    widget.bind("<MouseWheel>", scroll_function)
    for child in widget.winfo_children():
        enable_mouse_scroll(child, scroll_function)

avatars = (
    get_asset("avatars/avatar_orange.svg"),
    get_asset("avatars/avatar_blue.svg"),
    get_asset("avatars/avatar_green.svg"),
    get_asset("avatars/avatar_red.svg"),
    get_asset("avatars/avatar_purple.svg"),
    get_asset("avatars/avatar_brown.svg")
)



class Contact(BaseCard):
    def __init__(
            self,
            name: str,
            number: str,
            group: str,
            favorite: bool = False,
            window: Widget = None,
            favorites_only: bool = False,
            save_group: bool = False
        ):

        self.number = number.strip()
        self.group = group.strip()
        self.favorite = favorite
        self.favorites_only = favorites_only

        parent = window if window else contacts_frame
        super().__init__(name.strip(), parent, choice(avatars))
        shared.contacts_objects.append(self)

        self.edit_frame = None
        self.favorite_btn = None
        self.name_contact_box = None
        self.name_contact_copy = None
        self.number_contact_box = None
        self.number_contact_copy = None
        self.group_box = None
        self.not_name_error: Widget | None = None
        self.not_number_error: Widget | None = None
        self.len_name_error: Widget | None = None
        self.len_number_error: Widget | None = None

        self.favorite_img = PhotoImage(file=get_asset(r"contacts\favorite_button.svg"))
        self.favorite_img2 = PhotoImage(file=get_asset(r"contacts\favorite_button2.svg"))
        self.favorite_img3 = PhotoImage(file=get_asset(r"contacts\favorite_button3.svg"))

        self.create_widget()

        if not self.favorites_only:
            enable_mouse_scroll(self.frame)

        if save_group:
            self.append_contact_in_group()

        if self.favorites_only and window is not None:
            enable_mouse_scroll(self.frame, lambda event: window.master.yview_scroll(int(-event.delta / 120), "units"))

    def delete_contact_messagebox(self):
        MyMessagebox().question("آیا از حذف این مخاطب اطمینان دارید؟", "🗑 حذف مخاطب", self.delete_contact)

    def delete_contact(self):
        self.frame.destroy()

        contacts_data = read_json(CONTACTS_FILE)

        contacts_data = [
            contact for contact in contacts_data
            if not (contact["name"] == self.name and contact["number"] == self.number)
        ]

        write_json(contacts_data, CONTACTS_FILE)

        groups_data = read_json(GROUPS_FILE)

        for group in groups_data:
            if self.name in group["contacts"]:
                group["contacts"].remove(self.name)

        write_json(groups_data, GROUPS_FILE)

        shared.contacts_count.set(shared.contacts_count.get() - 1)

        if shared.contacts_count.get() == 0:
            show_empty_contacts_message()
            shared.contacts_count_label.place_forget()
            shared.contacts_count_text.place_forget()

    def create_widget(self):
        if not self.favorites_only:
            self.create_buttons(self.delete_contact_messagebox, self.edit_contact)

        self.favorite_btn = my_button(self.frame, image=self.favorite_img3 if self.favorite else self.favorite_img, x=95 if not self.favorites_only else 25, y=22, bg="#152238", width=24, height=24, activebackground="#152238", bd=0, command=self.toggle_favorite)

        self.favorite_btn.bind("<Enter>", lambda event: self.favorite_btn.config(image=self.favorite_img2 if not self.favorite else self.favorite_img3))
        self.favorite_btn.bind("<Leave>", lambda event: self.favorite_btn.config(image=self.favorite_img if not self.favorite else self.favorite_img3))

        self.favorite_btn.image = self.favorite_img3 if self.favorite else self.favorite_img

        display_name = shorten_text(self.name, max_width=130, font_name="Samim WOL", size=13)
        my_label(self.frame, text=display_name, x=537, y=34, bg="#152238", anchor=True, size=13)
        my_label(self.frame, text=self.number, x=253, y=22, bg="#152238", size=13)
        label_image(self.frame, get_asset(r"contacts\phone_label.svg"), x=220, y=23, bg="#152238")

    def append_contact_in_group(self):
        groups_data = read_json(GROUPS_FILE)
        for group in groups_data:
            if group["name"] == self.group:
                group["contacts"].append(self.name)

        write_json(groups_data, GROUPS_FILE)

    def edit_contact(self):
        self.edit_frame = Frame(shared.root, bg="#0D1729", width=650, height=490)
        self.edit_frame.place(x=230, y=90)

        my_label(self.edit_frame, text=":نام مخاطب", x=375, y=50, size=13)
        self.name_contact_box = my_entry_ctk(window=self.edit_frame, x=135, y=46, width=225, height=40)
        self.name_contact_box.insert(0, self.name)
        self.name_contact_copy = self.name_contact_box.get()

        my_label(self.edit_frame, text=":شماره مخاطب", x=375, y=150, size=13)
        self.number_contact_box = my_entry_ctk(window=self.edit_frame, x=135, y=146, width=225, height=40, justify="left")
        self.number_contact_box.insert(0, self.number)
        self.number_contact_copy = self.number_contact_box.get()

        my_label(self.edit_frame, text=":افزودن به گروه", x=375, y=250, size=13)
        self.group_box = CTkComboBox(self.edit_frame, values=shared.groups, width=225, height=40, corner_radius=10, font=("Vazir", 18), dropdown_font=("Vazir", 14), fg_color="#152238", border_color="#3A4A55", border_width=1, button_color="#0078d4", button_hover_color="#005a9e", dropdown_fg_color="#152238", dropdown_hover_color="#2d3a48", dropdown_text_color="white", text_color="white")
        self.group_box.set(self.group)

        self.group_box.place(x=134, y=248)
        self.group_box.bind("<KeyPress>", lambda event: "break")

        shared.active_frames.append(self.edit_frame)

        my_button_ctk(self.edit_frame, text="تایید", x=30, y=400, size=17, width=80, height=40, fg_color="green", hover_color="#006400", corner_radius=7, command=self.save_edited_contact)
        shared.root.bind("<Return>", lambda event: self.save_edited_contact())

        my_button_ctk(self.edit_frame, text="لغو", x=520, y=400, size=17, width=80, height=40, fg_color="red", hover_color="#8B0000", corner_radius=7, command=self.cancel_edit)

    def save_edited_contact(self):
        name = self.name_contact_box.get().strip()
        number = self.number_contact_box.get().strip()
        group = self.group_box.get()

        if len(name) <= 16 and self.len_name_error:
            self.len_name_error.destroy()
            self.len_name_error = None

        if len(number) <= 11 and self.len_number_error:
            self.len_number_error.destroy()
            self.len_number_error = None

        if not name:
            if self.not_name_error is None:
                self.not_name_error = my_label(self.edit_frame, x=160, y=90, text="لطفا نام مخاطب را وارد کنید", fg="#FF6060", size=11)

            if self.len_name_error:
                self.len_name_error.destroy()
                self.len_name_error = None

        else:
            if self.not_name_error:
                self.not_name_error.destroy()
                self.not_name_error = None

        if not number:
            if self.not_number_error is None:
                self.not_number_error = my_label(self.edit_frame, x=150, y=190, text="لطفا شماره مخاطب را وارد کنید", fg="#FF6060", size=11)

            if self.len_number_error:
                self.len_number_error.destroy()
                self.len_number_error = None

        else:
            if self.not_number_error:
                self.not_number_error.destroy()
                self.not_number_error = None

        if len(name) > 16 or len(number) > 11:
            if len(name) > 16:
                if self.len_name_error is None:
                    self.len_name_error = my_label(self.edit_frame, x=120, y=90, text="نام مخاطب نمیتواند بالای 16 کاراکتر باشد", fg="#FF6060", size=11)

            else:
                if self.len_name_error:
                    self.len_name_error.destroy()
                    self.len_name_error = None

            if len(number) > 11:
                if self.len_number_error is None:
                    self.len_number_error = my_label(self.edit_frame, x=117, y=190, text="شماره مخاطب نمیتواند بالای 11 رقم باشد", fg="#FF6060", size=11)

            else:
                if self.len_number_error:
                    self.len_number_error.destroy()
                    self.len_number_error = None
            return

        if name and number:
            contacts_data = read_json(CONTACTS_FILE)

            for contact in contacts_data:
                if contact["name"] == self.name_contact_copy and contact["number"] == self.number_contact_copy:
                    contact["name"] = name
                    contact["number"] = number
                    contact["group"] = group
                    break

            write_json(contacts_data, CONTACTS_FILE)

            groups_data = read_json(GROUPS_FILE)

            for group_data in groups_data:
                if self.name_contact_copy in group_data["contacts"]:
                    group_data["contacts"].remove(self.name_contact_copy)

            write_json(groups_data, GROUPS_FILE)

            self.frame.destroy()
            Contact(name, number, group, self.favorite, save_group=True)
            shared.root.unbind("<Return>")
            self.edit_frame.destroy()

    def cancel_edit(self):
        shared.root.unbind("<Return>")
        self.edit_frame.destroy()

    def toggle_favorite(self):
        self.favorite = not self.favorite

        contacts_data = read_json(CONTACTS_FILE)

        for contact in contacts_data:
            if contact["name"] == self.name and contact["number"] == self.number:
                contact["favorite"] = self.favorite
                break

        write_json(contacts_data, CONTACTS_FILE)

        for contact in shared.contacts_objects:
            if contact.name == self.name and contact.number == self.number:
                contact.update_favorite_button(self.favorite)
                contact.update_favorite_button(self.favorite)

    def update_favorite_button(self, favorite):
        if not self.frame.winfo_exists():
            return

        self.favorite = favorite

        if self.favorite:
            self.favorite_btn.config(image=self.favorite_img3)
            self.favorite_btn.image = self.favorite_img3
        else:
            self.favorite_btn.config(image=self.favorite_img)
            self.favorite_btn.image = self.favorite_img