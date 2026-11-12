from customtkinter import CTkComboBox, CTkSwitch
from tkinter import Frame, Widget, BooleanVar

from PhoneBook import shared

from PhoneBook.utils.widget_utils.button_utils import my_button_ctk
from PhoneBook.utils.path_utils import CONTACTS_FILE, GROUPS_FILE
from PhoneBook.utils.widget_utils.entry_util import my_entry_ctk
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.sound_utils import click_sound
from PhoneBook.utils.widget_utils.messagebox_util import MyMessagebox
from PhoneBook.utils.json_utils import read_json, write_json

from PhoneBook.models.contact import Contact, hide_empty_contacts_message
from PhoneBook.models.group import Group, group_avatars, hide_empty_groups_message

from PhoneBook.ui.views.menu_view import create_menu_view, create_menu_widgets
from PhoneBook.ui.views.favorites_view import FavoritesView
from PhoneBook.ui.views.groups_view import GroupsView



class CreateMenu:
    def __init__(self):
        self.menu_frame = create_menu_view()

        self.add_group_frame = None
        self.add_contact_btn_frame = None
        self.name_contact_box = None
        self.number_contact_box = None
        self.group_box = None
        self.name_group_box = None
        self.color_box = None
        self.pin_switch = None

        self.not_name_error = None
        self.not_number_error = None
        self.len_name_error = None
        self.len_number_error = None
        self.not_number_isdigit = None

        self.reset_error_widgets()

        (
            self.contacts_btn,
            self.favorites_btn,
            self.groups_btn,
            self.add_contact_btn,
            self.add_group_btn,
        ) = create_menu_widgets(
            self.menu_frame,
            self.show_contacts,
            self.show_favorites,
            self.show_groups,
            self.show_add_contact,
            self.show_add_group,
        )

    def changing_button_colors(self, active_button=None):
        buttons = {
            "ADD_CONTACT": self.add_contact_btn,
            "add_group_btn": self.add_group_btn,
            "contacts_btn": self.contacts_btn,
            "favorites_btn": self.favorites_btn,
            "groups_btn": self.groups_btn,
        }

        for name, button in buttons.items():
            if name != active_button:
                button.configure(fg_color="#112034", hover_color="#16243A",)

    def reset_error_widgets(self):
        self.not_name_error: Widget | None = None
        self.not_number_error: Widget | None = None
        self.len_name_error: Widget | None = None
        self.len_number_error: Widget | None = None
        self.not_number_isdigit: Widget | None = None

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

    def show_add_contact(self):
        self.changing_button_colors("ADD_CONTACT")
        self.clear_frames()
        self.hide_search_canvas()
        self.reset_error_widgets()

        self.add_contact_btn_frame = Frame(shared.root, bg="#0D1729", width=650, height=490)
        self.add_contact_btn_frame.place(x=230, y=90)

        my_label(self.add_contact_btn_frame, text=":نام مخاطب", x=375, y=50, size=13)
        self.name_contact_box = my_entry_ctk(self.add_contact_btn_frame, x=135, y=46, width=225, height=40, placeholder_text="...بنویسید ")

        my_label(self.add_contact_btn_frame, text=":شماره مخاطب", x=375, y=150, size=13)
        self.number_contact_box = my_entry_ctk(self.add_contact_btn_frame, x=135, y=146, width=225, height=40, justify="left", placeholder_text=" 09...")

        my_label(self.add_contact_btn_frame, text=":افزودن به گروه", x=375, y=250, size=13)
        self.group_box = CTkComboBox(self.add_contact_btn_frame, values=shared.groups, width=225, height=40, corner_radius=10, font=("Vazir", 18), dropdown_font=("Vazir", 14), fg_color="#152238", border_color="#3A4A55", border_width=1, button_color="#0078d4", button_hover_color="#005a9e", dropdown_fg_color="#152238", dropdown_hover_color="#2d3a48", dropdown_text_color="white", text_color="white")
        self.group_box.place(x=134, y=248)
        self.group_box.bind("<KeyPress>", lambda event: "break")

        shared.active_frames.append(self.add_contact_btn_frame)

        self.create_add_contact_buttons()

    def add_contact(self):
        name = self.name_contact_box.get().strip()
        number = self.number_contact_box.get().strip()
        group = self.group_box.get()

        if len(name) <= 16 and self.len_name_error:
            self.len_name_error.destroy()
            self.len_name_error = None

        if len(number) <= 11 and self.len_number_error:
            self.len_number_error.destroy()
            self.len_number_error = None

        if number.isdigit() and self.not_number_isdigit:
            self.not_number_isdigit.destroy()
            self.not_number_isdigit = None

        if not name.replace(" ", ""):

            if self.not_name_error is None:
                self.not_name_error = my_label(self.add_contact_btn_frame, x=160, y=90, text="لطفا نام مخاطب را وارد کنید", fg="#FF7575", size=11)

            if self.len_name_error:
                self.len_name_error.destroy()
                self.len_name_error = None

        else:
            if self.not_name_error:
                self.not_name_error.destroy()
                self.not_name_error = None

        if not number.replace(" ", ""):
            if self.not_number_error is None:
                self.not_number_error = my_label(self.add_contact_btn_frame, x=150, y=190, text="لطفا شماره مخاطب را وارد کنید", fg="#FF7575", size=11)

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
                    self.len_name_error = my_label(self.add_contact_btn_frame, x=120, y=90, text="نام مخاطب نمیتواند بالای 16 کاراکتر باشد", fg="#FF7575", size=11)

            else:
                if self.len_name_error:
                    self.len_name_error.destroy()
                    self.len_name_error = None

            if len(number) > 11:
                if self.len_number_error is None:
                    self.len_number_error = my_label(self.add_contact_btn_frame, x=117, y=190, text="شماره مخاطب نمیتواند بالای 11 رقم باشد", fg="#FF7575", size=11)

            else:
                if self.len_number_error:
                    self.len_number_error.destroy()
                    self.len_number_error = None

            return

        if number and not number.isdigit():
            if self.not_number_isdigit is None:
                self.not_number_isdigit = my_label(self.add_contact_btn_frame, x=110, y=190, text="شماره مخاطب نمیتواند از حروف تشکیل شده باشد", fg="#FF7575", size=10)

            return

        if name and number:
            contacts_data = read_json(CONTACTS_FILE)
            for contact in contacts_data:
                if contact["name"] == name and contact["number"] == number:
                    MyMessagebox().message(".این مخاطب از قبل وجود دارد", "باشه", "⚠️ مخاطب تکراری")
                    return

            contacts_data.append({"name": name, "number": number, "group": group, "favorite": False})
            Contact(name, number, group, save_group=True)
            shared.contacts_count_label.place(x=234, y=90)
            shared.contacts_count_text.place(x=278, y=87)

            write_json(contacts_data, CONTACTS_FILE)

            if shared.contacts_count.get() == 0:
                hide_empty_contacts_message()

            shared.contacts_count.set(value=shared.contacts_count.get() + 1)

            self.changing_button_colors("contacts_btn")
            self.contacts_btn.configure(fg_color="#182E65", hover_color="#193068")

            shared.root.unbind("<Return>")
            self.add_contact_btn_frame.destroy()

    def cancel_add_contact(self):
        shared.root.unbind("<Return>")
        self.add_contact_btn_frame.destroy()
        self.changing_button_colors("contacts_btn")
        self.contacts_btn.configure(fg_color="#182E65", hover_color="#193068")

        self.reset_error_widgets()

    def show_contacts(self):
        self.clear_frames()
        self.hide_search_canvas()
        self.reset_error_widgets()
        self.changing_button_colors("contacts_btn")
        self.add_contact_btn.place(x=18, y=380)
        self.add_group_btn.place_forget()

    def show_favorites(self):
        FavoritesView(self)

    def show_add_group(self):
        self.hide_search_canvas()
        self.reset_error_widgets()

        self.changing_button_colors("add_group_btn")

        if self.add_group_frame is not None:
            self.add_group_frame.destroy()

        self.add_group_frame = Frame(shared.root, bg="#0D1729", width=650, height=490)
        self.add_group_frame.place(x=230, y=90)

        my_label(self.add_group_frame, text=":نام گروه", x=390, y=54, size=13)
        self.name_group_box = my_entry_ctk(window=self.add_group_frame, x=150, y=50, width=225, height=40, placeholder_text="...بنویسید ")

        shared.active_frames.append(self.add_group_frame)

        pin_group = BooleanVar(value=False)
        self.pin_switch = CTkSwitch(self.add_group_frame, text="    :سنجاق کردن گروه", variable=pin_group, switch_height=25, switch_width=50, button_length=1, font=("Vazir", 17), text_color="white", corner_radius=12, fg_color="#3A4A55", progress_color="#0078d4", button_color="white", button_hover_color="#D1FAE5", hover=True, border_width=0, command=self.pin_group)
        self.pin_switch.place(x=248, y=155)

        my_label(self.add_group_frame, text=":رنگ پروفایل گروه", x=325, y=251, size=13)

        colors = ("رندوم", "آبی", "قهوه ای", "سبز", "نارنجی", "بنفش", "قرمز")
        self.color_box = CTkComboBox(self.add_group_frame, values=colors, width=156, height=40, corner_radius=10, font=("Vazir", 18), dropdown_font=("Vazir", 14), fg_color="#152238", border_color="#3A4A55", border_width=1, button_color="#0078d4", button_hover_color="#005a9e", dropdown_fg_color="#152238", dropdown_hover_color="#2d3a48", dropdown_text_color="white", text_color="white")
        self.color_box.place(x=150, y=249)
        self.color_box.bind("<KeyPress>", lambda event: "break")

        self.create_add_group_buttons()

    def cancel_add_group(self):
        shared.root.unbind("<Return>")
        self.add_group_frame.destroy()
        self.changing_button_colors("groups_btn")
        self.groups_btn.configure(fg_color="#182E65", hover_color="#193068")

        self.reset_error_widgets()

    @staticmethod
    def pin_group():
        if shared.sound.get():
            click_sound()

        MyMessagebox(420).message(".این قابلیت در نسخه‌های آینده اضافه خواهد شد ", "باشه", "🚧 به‌زودی")

    def add_group(self):
        name = self.name_group_box.get().strip()

        if len(name) <= 20 and self.len_name_error:
            self.len_name_error.destroy()
            self.len_name_error = None

        if not name.replace(" ", ""):
            if self.not_name_error is None:
                self.not_name_error = my_label(self.add_group_frame, x=180, y=93, text="لطفا نام گروه را وارد کنید", fg="#FF7575", size=11)

            if self.len_name_error:
                self.len_name_error.destroy()
                self.len_name_error = None

        else:
            if self.not_name_error:
                self.not_name_error.destroy()
                self.not_name_error = None

        if len(name) > 20:
            if self.len_name_error is None:
                self.len_name_error = my_label(self.add_group_frame, x=143, y=93, text="نام گروه نمیتواند بالای 20 کاراکتر باشد", fg="#FF7575", size=11)
            return

        else:
            if self.len_name_error:
                self.len_name_error.destroy()
                self.len_name_error = None

        if name:
            groups_data = read_json(GROUPS_FILE)
            for group in groups_data:
                if group["name"] == name:
                    MyMessagebox().message(".این گروه از قبل وجود دارد", "باشه", "⚠️ گروه تکراری")
                    return

            groups_data.append({
                "name": name,
                "contacts": [],
                "color": self.change_color(),
                "pin": bool(self.pin_switch.get()),
            })
            Group(name=name, color=self.change_color())

            write_json(groups_data, GROUPS_FILE)

            shared.groups.append(name)

            if shared.groups_count.get() == 0:
                hide_empty_groups_message()

            shared.groups_count.set(value=shared.groups_count.get() + 1)
            shared.groups_count_label.place(x=4, y=0)
            shared.groups_count_text.place(x=48, y=-3)

            self.changing_button_colors("groups_btn")
            self.groups_btn.configure(fg_color="#182E65", hover_color="#193068")

            shared.root.unbind("<Return>")
            self.add_group_frame.destroy()

    def show_groups(self):
        GroupsView(self)

    def create_add_group_buttons(self):
        my_button_ctk(self.add_group_frame, text="افزودن", x=30, y=400, size=17, width=80, height=40, fg_color="green", hover_color="#006400", corner_radius=7, command=self.add_group)
        shared.root.bind("<Return>", lambda event: self.add_group())
        my_button_ctk(self.add_group_frame, text="لغو", x=520, y=400, size=17, width=80, height=40, fg_color="red", hover_color="#D10000", corner_radius=7, command=self.cancel_add_group)

    def create_add_contact_buttons(self):
        my_button_ctk(self.add_contact_btn_frame, text="افزودن", x=30, y=400, size=17, width=80, height=40, fg_color="green", hover_color="#006400", corner_radius=7, command=self.add_contact)
        shared.root.bind("<Return>", lambda event: self.add_contact())
        my_button_ctk(self.add_contact_btn_frame, text="لغو", x=520, y=400, size=17, width=80, height=40, fg_color="red", hover_color="#D10000", corner_radius=7, command=self.cancel_add_contact)

    @staticmethod
    def hide_search_canvas():
        if not shared.search_canvas is None:
            shared.search_canvas.place_forget()

    @staticmethod
    def clear_frames():
        for frame in shared.active_frames:
            frame.destroy()

        shared.active_frames.clear()
