from customtkinter import CTkFrame
from PhoneBook import shared
from PhoneBook.utils.widget_utils.label_utils import label_image
from PhoneBook.utils.widget_utils.button_utils import button_image_ctk
from PhoneBook.utils.path_utils import get_asset
from PhoneBook.utils.widget_utils.label_utils import my_label
from PhoneBook.ui.title_bar import start_move, move_window



def create_menu_view():
    menu_frame = CTkFrame(shared.root, width=195, height=576, fg_color="#0E182A", border_color="#1B2A3D", border_width=1, corner_radius=10)
    menu_frame.place(x=12, y=12)

    return menu_frame


def create_menu_widgets(menu_frame, contact_btn_command, favorite_btn_command, group_btn_command, add_contact_btn_command, add_group_btn_command):
    frame_for_move = CTkFrame(menu_frame, fg_color="#0E182A", width=191, height=111)
    frame_for_move.place(x=2, y=5)
    frame_for_move.bind("<Button-1>", start_move)
    frame_for_move.bind("<B1-Motion>", move_window)

    logo = label_image(menu_frame, get_asset(r"icon_and_logo\logo.png"), x=54, y=28)
    logo.bind("<Button-1>", start_move)
    logo.bind("<B1-Motion>", move_window)

    my_label(menu_frame, text="دفترچه تلفن", x=45, y=116, size=14, fg="white", font="Samim WOL")

    contacts_btn = button_image_ctk(menu_frame, get_asset(r"menu_buttons\contacts_button.png"), x=18, y=185, width=98, height=40, bg_color="#182E65", hover_color="#193068", command=contact_btn_command)
    contacts_btn.bind("<Button-1>", lambda e: contacts_btn.configure(fg_color="#182E65", hover_color="#193068"))

    favorites_btn = button_image_ctk(menu_frame, get_asset(r"menu_buttons\favorites_button.png"), x=18, y=250, width=134, height=48, command=favorite_btn_command)
    favorites_btn.bind("<Button-1>", lambda e: favorites_btn.configure(fg_color="#182E65", hover_color="#193068"))

    groups_btn = button_image_ctk(menu_frame, get_asset(r"menu_buttons\groups_button.png"), x=18, y=315, width=92, height=38, command=group_btn_command)
    groups_btn.bind("<Button-1>", lambda e: groups_btn.configure(fg_color="#182E65", hover_color="#193068"))

    add_contact_btn = button_image_ctk(menu_frame, get_asset(r"menu_buttons\add_contact_button.png"), x=18, y=380, width=130, height=36, command=add_contact_btn_command)
    add_contact_btn.bind("<Button-1>", lambda e: add_contact_btn.configure(fg_color="#182E65", hover_color="#193068"))

    add_group_btn = button_image_ctk(menu_frame, get_asset(r"menu_buttons\add_group_button.png"), x=18, y=380, width=130, height=44, command=add_group_btn_command)
    add_group_btn.bind("<Button-1>", lambda e: add_group_btn.configure(fg_color="#182E65", hover_color="#193068"))
    add_group_btn.place_forget()

    return contacts_btn, favorites_btn, groups_btn, add_contact_btn, add_group_btn
