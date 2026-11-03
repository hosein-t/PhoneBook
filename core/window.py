from tkinter import Tk, Frame
from PhoneBook.utils.path_utils import get_asset
from PhoneBook.ui.button_commands import close_tab



def create_window():
    root = Tk()

    x = (root.winfo_screenwidth() - 900) // 2
    y = (root.winfo_screenheight() - 600) // 2

    root.geometry(f"900x600+{x}+{y - 50}")
    root.title("دفترچه تلفن")
    root.iconbitmap(get_asset(r"icon_and_logo\icon.ico"))
    root.overrideredirect(True)
    root.configure(bg="#0D1729")

    root.protocol("WM_DELETE_WINDOW", close_tab)

    Frame(root, bg="#0078d4", width=900, height=1).place(x=0, y=599)
    Frame(root, bg="#0078d4", width=1, height=600).place(x=0, y=0)
    Frame(root, bg="#0078d4", width=1, height=600).place(x=899, y=0)
    Frame(root, bg="#0078d4", width=900, height=1).place(x=0, y=0)

    return root
