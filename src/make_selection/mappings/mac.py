import os
import sys
import termios
import tty
from key_codes import KeyCode

ARROW_UP   = b"\x1b[A"
ARROW_DOWN = b"\x1b[B"
CMD_RIGHT  = b"\x05"
CTL_C      = b"\x03"
ENTER_PATTERNS     = b"\r\n"
BACKSPACE_PATTERNS = b"\x08\x7f"

def _is_searchable(key_press: bytes) -> bool:
    try:
        key_press = ord(key_press.decode())
        return (32 <= key_press and key_press <= 126)
    except:
        return False

def _read_key_press() -> bytes:
    try:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        # NOTE: Read up to 3 bytes for escape sequences.
        return os.read(fd, 3)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def getChar() -> tuple[KeyCode|None, str|None]:
    key_press: bytes = _read_key_press()

    key_code = None
    char = None
    if key_press == ARROW_UP:
        key_code = KeyCode.UP
    elif key_press == ARROW_DOWN:
        key_code = KeyCode.DOWN
    elif key_press in ENTER_PATTERNS:
        key_code = KeyCode.SELECT
    elif key_press == CMD_RIGHT:
        key_code = KeyCode.SELECT_MULTI
    elif key_press == CTL_C:
        key_code = KeyCode.CANCEL
    elif key_press in BACKSPACE_PATTERNS:
        key_code = KeyCode.DELETE_CHAR
    elif _is_searchable(key_press):
        key_code = KeyCode.SEARCHABLE
        char = key_press.decode()
    return key_code, char
