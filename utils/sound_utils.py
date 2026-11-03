from winsound import PlaySound, SND_FILENAME, SND_ASYNC
from PhoneBook.utils.path_utils import get_asset



def click_sound() -> None:
    PlaySound(get_asset(r"sounds\click.wav"), SND_FILENAME | SND_ASYNC)


def close_sound() -> None:
    PlaySound(get_asset(r"sounds\close_sound.wav"), SND_FILENAME | SND_ASYNC)


def messagebox_sound() -> None:
    PlaySound(get_asset(r"sounds\messagebox.wav"), SND_FILENAME | SND_ASYNC)