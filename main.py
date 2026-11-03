from tkinter import BooleanVar, IntVar

from PhoneBook import shared
from PhoneBook.models.contact import create_contacts_ui
from PhoneBook.ui.menu import CreateMenu
from PhoneBook.ui.views.contacts_view import initialize_contacts_view
from PhoneBook.ui.views.login_view import LoginView
from PhoneBook.ui.title_bar import CreateTitleBar
from PhoneBook.core.data_manager import create_data_files, open_data_files
from PhoneBook.core.app_resources import load_fonts, initialize_shared_data
from PhoneBook.core.taskbar_app_icon import configure_window_style
from PhoneBook.core.window import create_window



def main():
    # Window
    shared.root = create_window()
    configure_window_style()

    # Resources
    load_fonts()

    # Data
    create_data_files()
    data, contacts_data, groups_data = open_data_files()
    initialize_shared_data(data, groups_data)

    # Shared state
    shared.contacts_count = IntVar(value=len(contacts_data))
    shared.groups_count = IntVar(value=len(groups_data) - 1)
    shared.sound = BooleanVar(value=data["sound"])
    shared.pin = BooleanVar(value=data["pin"])

    # UI
    create_contacts_ui()
    CreateTitleBar()
    CreateMenu()
    initialize_contacts_view(contacts_data)

    if not shared.registered:
        LoginView()

    return shared.root



if __name__ == "__main__":
    shared.root = main()
    shared.root.mainloop()
