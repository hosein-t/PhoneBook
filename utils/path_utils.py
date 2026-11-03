import sys
import os



if getattr(sys, "frozen", False):
    BASE_DIR = getattr(sys, "_MEIPASS")
    EXEC_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)) )
    EXEC_DIR = BASE_DIR


def get_asset(filename: str) -> str:
    return os.path.join(BASE_DIR, "assets", filename)


DATA_DIR = os.path.join(EXEC_DIR, "data")
SETTING_FILE = os.path.join(DATA_DIR, "setting.json")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")
GROUPS_FILE = os.path.join(DATA_DIR, "groups.json")