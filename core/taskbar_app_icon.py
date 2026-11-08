import ctypes
from PhoneBook import shared



def configure_window_style():
    shared.root.update_idletasks()

    user32 = ctypes.windll.user32

    get_parent = getattr(user32, "GetParent")
    get_window_long = getattr(user32, "GetWindowLongW")
    set_window_long = getattr(user32, "SetWindowLongW")

    window_id = get_parent(shared.root.winfo_id())
    window_style = get_window_long(window_id, -20)

    set_window_long(window_id, -20, (window_style & ~0x00000080) | 0x00040000)

    shared.root.withdraw()
    shared.root.after(10, shared.root.deiconify)
