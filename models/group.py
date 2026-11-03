from random import choice

from PhoneBook import shared
from PhoneBook.models.base_card import BaseCard
from PhoneBook.models.contact import enable_mouse_scroll
from PhoneBook.utils.path_utils import get_asset, GROUPS_FILE, CONTACTS_FILE
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.widget_utils.messagebox_util import MyMessagebox
from PhoneBook.utils.text_util import shorten_text
from PhoneBook.utils.json_utils import read_json, write_json



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

    def edit_group(self):
        """
        نکته:

        باید در اینجا لیست shared.groups اپدیت شه
        """
