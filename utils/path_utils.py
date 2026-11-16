import sys
import os



if getattr(sys, "frozen", False):
    BASE_DIR = getattr(sys, "_MEIPASS")
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


APP_DATA_DIR = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
EXEC_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else BASE_DIR


def get_asset(filename: str) -> str:
    return os.path.join(BASE_DIR, "assets", filename)


DATA_DIR = os.path.join(APP_DATA_DIR, "PhoneBook", "data")
SETTING_FILE = os.path.join(DATA_DIR, "setting.json")
CONTACTS_FILE = os.path.join(DATA_DIR, "contacts.json")
GROUPS_FILE = os.path.join(DATA_DIR, "groups.json")