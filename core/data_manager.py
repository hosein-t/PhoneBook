import os
from PhoneBook.utils.path_utils import DATA_DIR, SETTING_FILE, CONTACTS_FILE, GROUPS_FILE
from PhoneBook.utils.json_utils import read_json, write_json



def create_data_files() -> None:
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

    if not os.path.isfile(SETTING_FILE):
        settings_data = {
            "registered": False,
            "sound": True,
            "pin": False,
            "click_count": 0,
        }

        write_json(settings_data, SETTING_FILE)

    if not os.path.isfile(CONTACTS_FILE):
        write_json([], CONTACTS_FILE)

    if not os.path.isfile(GROUPS_FILE):
        groups_data = {
            "name": "بدون گروه",
            "contacts": [],
            "color": None,
            "pin": False,
        }

        write_json([groups_data], GROUPS_FILE)

def open_data_files() -> dict:
    data = read_json(SETTING_FILE)
    contacts_data = read_json(CONTACTS_FILE)
    groups_data = read_json(GROUPS_FILE)

    return data, contacts_data, groups_data