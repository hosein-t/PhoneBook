from PhoneBook import shared
from PhoneBook.utils.path_utils import SETTING_FILE
from PhoneBook.utils.json_utils import read_json, write_json



def close_tab():
    data = read_json(SETTING_FILE)

    data["sound"] = shared.sound.get()
    data["pin"] = shared.pin.get()
    data["registered"] = shared.registered
    data["click_count"] = shared.click_count

    write_json(data, SETTING_FILE)

    if shared.sound.get():
        shared.root.after(230)

    shared.root.destroy()