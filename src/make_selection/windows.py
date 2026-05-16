import msvcrt
import ctypes
from key_codes import KeyCode

stdout = -11
enable_ansi_codes = 7
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(stdout), enable_ansi_codes)

SPECIAL_KEY = 224
ARROW_UP    = 72
ARROW_DOWN  = 80
TAB         = 9
ENTER       = 13
CTL_C       = 3
BACKSPACE   = 8

def isSearchable(char: int) -> bool:
    return (32 <= char and char <= 126)
    
def getChar() -> tuple[KeyCode|None, str|None]:
    key_press = ord(msvcrt.getch())
    if key_press == SPECIAL_KEY:
        key_press = ord(msvcrt.getch())

    key_code = None
    char = None
    if key_press == ARROW_UP:
        key_code = KeyCode.UP
    elif key_press == ARROW_DOWN:
        key_code = KeyCode.DOWN
    elif key_press == ENTER:
        key_code = KeyCode.SELECT
    elif key_press == CTL_C:
        key_code = KeyCode.CANCEL
    elif isSearchable(key_press):
        key_code = KeyCode.SEARCHABLE
        char = chr(key_press)
    elif key_press == BACKSPACE:
        key_code = KeyCode.DELETE_CHAR
    elif key_press == TAB:
        key_code = KeyCode.SELECT_MULTI
    return key_code, char
