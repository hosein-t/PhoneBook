from customtkinter import CTkLabel
from tkinter import Frame, Canvas

from PhoneBook import shared
from PhoneBook.utils.path_utils import GROUPS_FILE
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.utils.widget_utils.scrollbar_util import MyScrollbar
from PhoneBook.utils.json_utils import read_json
from PhoneBook.models.group import Group, scroll_groups
from PhoneBook.models.contact import enable_mouse_scroll



class GroupsView:
    def __init__(self, menu):
        self.menu = menu

        self.group_frame = None
        self.group_scrollbar = None
        self.groups_frame = None

        self.prepare_menu()
        self.create_groups_frame()
        self.create_groups_canvas()
        self.add_groups_to_frame()

    def prepare_menu(self):
        self.menu.changing_button_colors("groups_btn")
        self.menu.clear_frames()
        self.menu.reset_error_widgets()
        self.menu.hide_search_canvas()
        self.menu.add_group_btn.place(x=18, y=380)
        self.menu.add_contact_btn.place_forget()

    def create_groups_frame(self):
        self.groups_frame = Frame(shared.root, bg="#0D1729", width=660, height=475)
        self.groups_frame.place(x=230, y=90)
        shared.active_frames.append(self.groups_frame)

    def create_groups_canvas(self):
        shared.groups_canvas = Canvas(self.groups_frame, bg="#0D1729", highlightthickness=0)
        shared.groups_canvas.place(x=0, y=40, width=660, height=435)
        self.group_scrollbar = MyScrollbar(self.groups_frame, shared.groups_canvas, height=441)

        self.group_frame = Frame(shared.groups_canvas, bg="#0D1729")
        shared.group_frame = self.group_frame

        shared.groups_canvas.create_window((0, 0), window=self.group_frame, anchor="nw", width=630)
        shared.groups_canvas.config(yscrollcommand=self.group_scrollbar.scrollbar.set)
        self.group_frame.bind("<Configure>", self.on_frame_configure)

        enable_mouse_scroll(self.group_frame, lambda event: scroll_groups(event, self.group_frame, shared.groups_canvas))

    def on_frame_configure(self, _):
        shared.groups_canvas.configure(scrollregion=shared.groups_canvas.bbox("all"))

        if len(self.group_frame.winfo_children()) > 5:
            self.group_scrollbar.scrollbar.place(x=630, y=35)
        else:
            self.group_scrollbar.scrollbar.place_forget()

    def add_groups_to_frame(self):
        groups_data = read_json(GROUPS_FILE)

        shared.groups_count.set(sum(1 for group in groups_data if group["name"] != "بدون گروه"))
        shared.groups_count_text = my_label(self.groups_frame, text=":تعداد گروه‌ها", x=48, y=-3, size=11, fg="#AAB7CC", font="Samim WOL")
        shared.groups_count_label = CTkLabel(self.groups_frame, textvariable=shared.groups_count, width=38, height=24, fg_color="#292342", text_color="#D0C4FF", font=("TkFixedFont", 14, "bold"), corner_radius=12, border_width=1, border_color="#62558F")
        shared.groups_count_label.place(x=4, y=0)

        if shared.groups_count.get() == 0:
            shared.groups_count_label.place_forget()
            shared.groups_count_text.place_forget()

        has_group = False
        for group in groups_data:
            if group["name"] == "بدون گروه":
                continue
            Group(group["name"], color=group["color"])
            has_group = True

        if not has_group:
            shared.L5 = my_label(self.groups_frame, x=160, y=150, text="!هیچ گروهی ساخته نشده است", bg="#0D1729", fg="#7DD3FC", size=18, font="Samim WOL")
            shared.L6 = my_label(self.groups_frame, x=73, y=200, text=".برای ساخت گروه جدید، روی گزینه «ساخت گروه» در سمت چپ صفحه کلیک کنید", bg="#0D1729", fg="gray", size=11, font="Samim WOL")
