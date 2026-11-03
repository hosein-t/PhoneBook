import ctypes
from PhoneBook import shared
from PhoneBook.utils.path_utils import get_asset



def load_fonts():
    gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
    add_font_resource_ex = getattr(gdi32, "AddFontResourceExW")

    add_font_resource_ex(get_asset(r"fonts\Vazir.ttf"), 0x10, 0)
    add_font_resource_ex(get_asset(r"fonts\Samim.ttf"), 0x10, 0)

def initialize_shared_data(data, groups_data):
    shared.click_count = data["click_count"]
    shared.registered = data["registered"]
    shared.groups = [group["name"] for group in groups_data]