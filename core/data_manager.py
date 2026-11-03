import os
from PhoneBook.utils.path_utils import DATA_DIR, SETTING_FILE, CONTACTS_FILE, GROUPS_FILE
from PhoneBook.utils.json_utils import read_json, write_json



def create_data_files():
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    if not os.path.isfile(SETTING_FILE):
        data = {"registered": False, "sound": True, "pin": False, "click_count": 0}
        write_json(data, SETTING_FILE)

    if not os.path.isfile(CONTACTS_FILE):
        write_json([], CONTACTS_FILE)

    if not os.path.isfile(GROUPS_FILE):
        write_json([{"name": "بدون گروه", "contacts": [], "color": None}], GROUPS_FILE)


def open_data_files():
    data = read_json(SETTING_FILE)
    contacts_data = read_json(CONTACTS_FILE)
    groups_data = read_json(GROUPS_FILE)

    return data, contacts_data, groups_data