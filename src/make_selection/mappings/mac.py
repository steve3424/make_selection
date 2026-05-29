import os
import sys
import termios
import tty
from ..key_codes import KeyCode

SPECIAL_KEY = None # NOTE: For cli tool
ARROW_UP   = b"\x1b[A"
ARROW_DOWN = b"\x1b[B"
OPT_RIGHT_PATTERNS  = (b"\x1b\x1b[C", "\x1bf")
CTL_C      = b"\x03"
ENTER_PATTERNS     = (b"\r", b"\n", b"\r\n")
BACKSPACE_PATTERNS = (b"\x08", b"\x7f")

def isSearchable(key_press: bytes) -> bool:
    try:
        key_press = ord(key_press.decode())
        return (32 <= key_press and key_press <= 126)
    except:
        return False

def readKeyPress() -> bytes:
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        # NOTE: Read up to 4 bytes for escape sequences.
        return os.read(fd, 4)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def getChar() -> tuple[KeyCode|None, str|None]:
    key_press: bytes = readKeyPress()

    key_code = None
    char = None
    if key_press == ARROW_UP:
        key_code = KeyCode.UP
    elif key_press == ARROW_DOWN:
        key_code = KeyCode.DOWN
    elif key_press in ENTER_PATTERNS:
        key_code = KeyCode.SELECT
    elif key_press in OPT_RIGHT_PATTERNS:
        key_code = KeyCode.SELECT_MULTI
    elif key_press == CTL_C:
        key_code = KeyCode.CANCEL
    elif key_press in BACKSPACE_PATTERNS:
        key_code = KeyCode.DELETE_CHAR
    elif isSearchable(key_press):
        key_code = KeyCode.SEARCHABLE
        char = key_press.decode()
    return key_code, char
