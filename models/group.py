from random import choice

from tkinter import Frame, BooleanVar, Widget
from customtkinter import CTkSwitch, CTkComboBox

from PhoneBook import shared
from PhoneBook.models.base_card import BaseCard
from PhoneBook.models.contact import enable_mouse_scroll
from PhoneBook.utils.path_utils import get_asset, GROUPS_FILE, CONTACTS_FILE
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.widget_utils.messagebox_util import MyMessagebox
from PhoneBook.utils.widget_utils.entry_util import my_entry_ctk
from PhoneBook.utils.widget_utils.button_utils import my_button_ctk
from PhoneBook.utils.text_util import shorten_text
from PhoneBook.utils.json_utils import read_json, write_json
from PhoneBook.utils.sound_utils import click_sound



def show_empty_groups_message():
    shared.L5 = my_label(shared.GROUPS_frame, text="!هیچ گروهی ساخته نشده است", x=160, y=150, bg="#0D1729", fg="#7DD3FC", size=18, font="Samim WOL")
    shared.L6 = my_label(shared.GROUPS_frame, text=".برای ساخت گروه جدید، روی گزینه «ساخت گروه» در سمت چپ صفحه کلیک کنید", x=73, y=200, bg="#0D1729", fg="gray", size=11, font="Samim WOL")

def hide_empty_groups_message():
    if shared.L5:
        shared.L5.destroy()
        shared.L5 = None
    if shared.L6:
        shared.L6.destroy()
        shared.L6 = None

def scroll_groups(event, group_frame, group_canvas):
    if len(group_frame.winfo_children()) > 5:
        group_canvas.yview_scroll(int(-event.delta / 120), "units")

group_avatars = (
    get_asset("group_avatars/avatar_orange.svg"),
    get_asset("group_avatars/avatar_blue.svg"),
    get_asset("group_avatars/avatar_green.svg"),
    get_asset("group_avatars/avatar_red.svg"),
    get_asset("group_avatars/avatar_purple.svg"),
    get_asset("group_avatars/avatar_brown.svg")
)



class Group(BaseCard):
    def __init__(self, name: str, color: str):
        self.color = color or choice(group_avatars)
        super().__init__(name.strip(), shared.group_frame, self.color)
        shared.groups_objects.append(self)

        self.edit_frame = None
        self.name_group_copy = None
        self.name_group_box = None
        self.color_box = None
        self.pin_switch = None
        self.not_name_error: Widget | None = None
        self.not_number_error: Widget | None = None
        self.len_name_error: Widget | None = None
        self.len_number_error: Widget | None = None

        hide_empty_groups_message()

        self.create_buttons(self.delete_group_messagebox, self.edit_group)
        self.create_widget()

        enable_mouse_scroll(self.frame, lambda event: scroll_groups(event, shared.group_frame, shared.groups_canvas))

    def create_widget(self):
        group_contact_count = []

        groups_data = read_json(GROUPS_FILE)

        for group in groups_data:
            if group["name"] == self.name:
                group_contact_count = group["contacts"]
                break

        display_name = shorten_text(self.name, max_width=230, font_name="Samim WOL", size=16)
        my_label(self.frame, text=display_name, x=535, y=34, bg="#152238", anchor=True, size=16, font="Samim WOL")
        my_label(self.frame, text=len(group_contact_count), x=250, y=22, bg="#152238", fg="#8ADCFF", size=11)
        my_label(self.frame, text="مخاطب", x=200, y=22, bg="#152238", fg="#8ADCFF", size=11)

    def delete_group_messagebox(self):
        MyMessagebox().question("آیا از حذف این گروه اطمینان دارید؟", "🗑 حذف گروه", self.delete_group)

    def delete_group(self):
        self.frame.destroy()

        shared.groups.remove(self.name)

        groups_data = read_json(GROUPS_FILE)
        groups_data = [group for group in groups_data if group["name"] != self.name]
        write_json(groups_data, GROUPS_FILE)

        contacts_data = read_json(CONTACTS_FILE)

        for contact in contacts_data:
            if contact["group"] == self.name:
                contact["group"] = "بدون گروه"

        write_json(contacts_data, CONTACTS_FILE)

        shared.groups_count.set(shared.groups_count.get() - 1)

        if shared.groups_count.get() == 0:
            show_empty_groups_message()
            shared.groups_count_label.place_forget()
            shared.groups_count_text.place_forget()

    @staticmethod
    def pin_group():
        if shared.sound.get():
            click_sound()

        MyMessagebox(420).message(".این قابلیت در نسخه‌های آینده اضافه خواهد شد ", "باشه", "🚧 به‌زودی")

    def edit_group(self):
        self.edit_frame = Frame(shared.root, bg="#0D1729", width=650, height=490)
        self.edit_frame.place(x=230, y=90)

        my_label(self.edit_frame, text=":نام گروه", x=390, y=54, size=13)
        self.name_group_box = my_entry_ctk(window=self.edit_frame, x=150, y=50, width=225, height=40, placeholder_text="...بنویسید ")
        self.name_group_box.insert(0, self.name)
        self.name_group_copy = self.name_group_box.get()

        pin_group = BooleanVar(value=False)
        self.pin_switch = CTkSwitch(self.edit_frame, text="    :سنجاق کردن گروه", variable=pin_group, switch_height=25, switch_width=50, button_length=1, font=("Vazir", 17), text_color="white", corner_radius=12, fg_color="#3A4A55", progress_color="#0078d4", button_color="white", button_hover_color="#D1FAE5", hover=True, border_width=0, command=self.pin_group)
        self.pin_switch.place(x=248, y=155)

        my_label(self.edit_frame, text=":رنگ پروفایل گروه", x=325, y=251, size=13)

        colors = ("رندوم", "آبی", "قهوه ای", "سبز", "نارنجی", "بنفش", "قرمز")
        self.color_box = CTkComboBox(self.edit_frame, values=colors, width=156, height=40, corner_radius=10, font=("Vazir", 18), dropdown_font=("Vazir", 14), fg_color="#152238", border_color="#3A4A55", border_width=1, button_color="#0078d4", button_hover_color="#005a9e", dropdown_fg_color="#152238", dropdown_hover_color="#2d3a48", dropdown_text_color="white", text_color="white")
        self.color_box.place(x=150, y=249)
        self.color_box.bind("<KeyPress>", lambda event: "break")

        color_names = {
            group_avatars[1]: "آبی",
            group_avatars[5]: "قهوه ای",
            group_avatars[2]: "سبز",
            group_avatars[0]: "نارنجی",
            group_avatars[4]: "بنفش",
            group_avatars[3]: "قرمز"
        }

        self.color_box.set(color_names.get(self.color, "رندوم"))

        my_button_ctk(self.edit_frame, text="تایید", x=30, y=400, size=17, width=80, height=40, fg_color="green", hover_color="#006400", corner_radius=7, command=self.save_edited_group)
        shared.root.bind("<Return>", lambda event: self.save_edited_group())

        my_button_ctk(self.edit_frame, text="لغو", x=520, y=400, size=17, width=80, height=40, fg_color="red", hover_color="#8B0000", corner_radius=7, command=self.cancel_edit)

    def save_edited_group(self):
        name = self.name_group_box.get().strip()
        pin = bool(self.pin_switch.get())
        color = self.change_color()

        if len(name) <= 20 and self.len_name_error:
            self.len_name_error.destroy()
            self.len_name_error = None

        if not name.replace(" ", ""):
            if self.not_name_error is None:
                self.not_name_error = my_label(self.edit_frame, x=180, y=93, text="لطفا نام گروه را وارد کنید", fg="#FF7575", size=11)

            if self.len_name_error:
                self.len_name_error.destroy()
                self.len_name_error = None

        else:
            if self.not_name_error:
                self.not_name_error.destroy()
                self.not_name_error = None

        if len(name) > 20:
            if self.len_name_error is None:
                self.len_name_error = my_label(self.edit_frame, x=143, y=93, text="نام گروه نمیتواند بالای 20 کاراکتر باشد", fg="#FF7575", size=11)
            return

        else:
            if self.len_name_error:
                self.len_name_error.destroy()
                self.len_name_error = None

        if name:
            groups_data = read_json(GROUPS_FILE)

            for group in groups_data:
                if group["name"] == name and name != self.name_group_copy:
                    MyMessagebox().message(".این گروه از قبل وجود دارد", "باشه", "⚠️ گروه تکراری")
                    return

                if group["name"] == self.name_group_copy:
                    group["name"] = name
                    group["color"] = color
                    group["pin"] = pin

            write_json(groups_data, GROUPS_FILE)

            contacts_data = read_json(CONTACTS_FILE)

            for contact in contacts_data:
                if contact["group"] == self.name_group_copy:
                    contact["group"] = name

            write_json(contacts_data, CONTACTS_FILE)

            for group in shared.groups:
                if group == self.name_group_copy:
                    shared.groups[shared.groups.index(group)] = name

            self.frame.destroy()
            Group(name, color)
            shared.root.unbind("<Return>")
            self.edit_frame.destroy()

    def cancel_edit(self):
        shared.root.unbind("<Return>")
        self.edit_frame.destroy()

    def change_color(self):
        colors = {
            "آبی": group_avatars[1],
            "قهوه ای": group_avatars[5],
            "سبز": group_avatars[2],
            "نارنجی": group_avatars[0],
            "قرمز": group_avatars[3],
            "بنفش": group_avatars[4],
        }

        return colors.get(self.color_box.get())
