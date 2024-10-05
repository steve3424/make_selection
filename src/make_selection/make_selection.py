"""
Module for interactive command line menu. Simply accepts a list of str-able objects
and allows user to select using arrow keys.

Ansi escape codes are used as described here: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
"""
# TODO: work on all platforms
# TODO: multi_select: Maintain original index for re-insertion.
# TODO: multi_select: TAB switches to delete mode.
import sys
if sys.platform != "win32":
    raise NotImplementedError("This module is only available on Windows.")
import msvcrt
import ctypes
from typing import Any
from copy import copy
from enum import Enum

stdout = -11
enable_ansi_codes = 7
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(stdout), enable_ansi_codes)

ANSI_MOVE_CURSOR             = "\x1b[{up}F\r\x1b[{right}C"
ANSI_HIGHLIGHT               = "\x1b[30;47m"
ANSI_HIGHLIGHT_SEARCH_STRING = "\x1b[95;47m"
ANSI_YELLOW                  = "\x1b[93m"
ANSI_BLUE                    = "\x1b[94m"
ANSI_MAGENTA                 = "\x1b[95m"
ANSI_GREEN                   = "\x1b[92m"
ANSI_RESET                   = "\x1b[0m"

SPECIAL_KEY = 224
UP_ARROW    = 72
DOWN_ARROW  = 80
ENTER_KEY   = 13
CTL_C       = 3
BACKSPACE   = 8
SPACEBAR    = 32
CTL_RIGHT   = 116

class Mode(Enum):
    NORMAL = 0
    MULTI_SELECT = 1
    MULTI_DELETE = 2

class Option:
    def __init__(self, obj: Any, sub_string_start: int=0) -> None:
        self.value = obj
        self.sub_string_start = sub_string_start

class Menu:
    def __init__(self, options: list, label: str, window_size: int=10, multi_select: bool=False) -> None:
        assert options
        assert label
        assert 1 <= window_size and window_size <= 25
        window_size = min((len(options)), window_size)

        self.options_original = [Option(op) for op in options]
        self.options_current = copy(self.options_original)
        self.options_selected = []
        self.search_string = ""
        self.label = label
        self.selected_index = 0
        self.window_top = 0
        self.window_size_original = window_size
        self.window_size_current = window_size
        self.help_string_multi_select = "Enter: Select, Ctl+C: Cancel, Ctl\u2192: Done"
        self.help_string_normal = "Enter: Select, Ctl+C: Cancel"
        if multi_select:
            self.mode = Mode.MULTI_SELECT
            self.help_string = self.help_string_multi_select
        else:
            self.mode = Mode.NORMAL
            self.help_string = self.help_string_normal

    def show(self):
        self.printMenu()
        while True:
            something_changed = False
            char = self.getChar()
            if char == SPECIAL_KEY:
                char = self.getChar()
                if char == CTL_RIGHT:
                    if self.mode == Mode.MULTI_SELECT:
                        self.printSelected()
                        return self.multiSelectGetValues(self.options_selected)
                elif 1 < len(self.options_current):
                    # NOTE: Update selected index
                    if char == UP_ARROW:
                        self.selected_index = (self.selected_index - 1) % len(self.options_current)
                        something_changed = True
                    elif char == DOWN_ARROW:
                        self.selected_index = (self.selected_index + 1) % len(self.options_current)
                        something_changed = True
                
                    # NOTE: Update window
                    if something_changed:
                        bottom = self.window_top + self.window_size_current
                        if self.selected_index < self.window_top:
                            self.window_top = self.selected_index
                        elif bottom <= self.selected_index:
                            self.window_top = self.selected_index - self.window_size_current + 1
            elif self.isSearchableChar(char):
                char = chr(char)
                self.search_string = f"{self.search_string}{char}".lstrip()
                if self.search_string:
                    print(char, end="", flush=True)
                    self.search(self.options_current)
                    something_changed = True
            elif char == BACKSPACE and 0 < len(self.search_string):
                self.search_string = self.search_string[:-1]
                # NOTE: Move left once ([1D), print space, move left again
                print("\x1b[1D \x1b[1D", end="", flush=True)
                self.search(self.options_original)
                something_changed = True
            elif char == ENTER_KEY and self.options_current:
                if self.mode == Mode.MULTI_SELECT:
                    self.multiSelectAdd()
                    something_changed = True
                elif self.mode == Mode.NORMAL:
                    self.printSelected()
                    return self.options_current[self.selected_index].value
            elif char == CTL_C:
                self.clearMenu()
                print("cancelled")
                return None

            if something_changed:
                self.clearMenu()
                self.printMenu()

    def search(self, search_list: list) -> None:
        found_options = []
        for o in search_list:
            found_i = str(o.value).lower().find(self.search_string.lower())
            if found_i != -1:
                o.sub_string_start = found_i
                found_options.append(o)
        self.options_current = found_options
        self.resetWindow()

    def multiSelectAdd(self) -> None:
        selected_option = self.options_current[self.selected_index]
        self.options_current.remove(selected_option)
        self.options_original.remove(selected_option)
        self.options_selected.append(selected_option)
        self.resetWindow()

    def multiSelectGetValues(self, options: list[Option]) -> list[Any]:
        return [op.value for op in options]

    def getChar(self) -> int:
        return ord(msvcrt.getch())

    def isSearchableChar(self, char):
        return (32 <= char and char <= 126)
    
    def resetWindow(self):
        self.window_top = 0
        self.selected_index = 0
        self.window_size_current = min((len(self.options_current), self.window_size_original))

    def clearMenu(self):
        """
        Clears from beginning of current line to end of screen (not end of line).
        This assumes the cursor is on the top line (label), which is currently always true.

        [0G move cursor to column 0.
        [J clears to end of screen (not end of line).
        """
        print("\x1b[0G\x1b[J", end="", flush=True)

    def printMenu(self):
        header = f"{ANSI_BLUE}{self.label}>{ANSI_RESET}{self.search_string}"
        header_num_lines = 1
        if self.mode == Mode.MULTI_SELECT:
            header += f"\n{ANSI_GREEN}{len(self.options_selected)} items in list!{ANSI_RESET}"
            header_num_lines = 2
        print(header)

        bottom = self.window_top + self.window_size_current
        if not self.options_current:
            print(f"{ANSI_BLUE}no matches found{ANSI_RESET}")
            # NOTE: window size is 0 here after empty search, but we are printing 1 line
            #       so we need to set it so the footer prints correctly
            self.window_size_current = 1
        else:
            for i in range(self.window_top, bottom):
                option_to_print = str(self.options_current[i].value)
                highlight_beg = self.options_current[i].sub_string_start
                highlight_end = highlight_beg + len(self.search_string)
                opt_beg = option_to_print[0 : highlight_beg]
                opt_mid = option_to_print[highlight_beg : highlight_end]
                opt_end = option_to_print[highlight_end :]
                if i == self.selected_index:
                    option_to_print = f"{ANSI_HIGHLIGHT}{opt_beg}{ANSI_HIGHLIGHT_SEARCH_STRING}{opt_mid}{ANSI_HIGHLIGHT}{opt_end}{ANSI_RESET}"
                else:
                    option_to_print = f"{opt_beg}{ANSI_MAGENTA}{opt_mid}{ANSI_RESET}{opt_end}"
                print(option_to_print)

        footer = f"{ANSI_YELLOW}{self.help_string}{ANSI_RESET}\n"
        footer_num_lines = 1
        print(f"{footer}{ANSI_MOVE_CURSOR.format(up=self.window_size_current + header_num_lines + footer_num_lines, right=len(self.label) + len(self.search_string) + 1)}", end="", flush=True)

    def printSelected(self):
        self.clearMenu()
        if self.mode == Mode.MULTI_SELECT:
            if len(self.options_selected) == 1:
                print(f"{self.label}> ({len(self.options_selected)} item) {self.multiSelectGetValues(self.options_selected)}")
            else:
                print(f"{self.label}> ({len(self.options_selected)} items) [{self.options_selected[0].value}, ...]")
        else:
            print(f"{self.label}> {self.options_current[self.selected_index].value}")

def makeSelection(options: list[Any], label: str, window_size: int=None, multi_select: bool=False) -> Any:
    """
    Entry point for menu selection.

    Parameters
    ----------
    options
        List of str-able objects.
    label
        Label to describe the items being selected.
    window_size
        Max number of items to show at once.
    multi_select
        Select list of items.

    Returns
    -------
    Selected value or list of selected values.
    """
    if window_size:
       return Menu(options, label, window_size=window_size, multi_select=multi_select).show()
    else:
       return Menu(options, label, multi_select=multi_select).show()

if __name__ == "__main__":
    print(f"Returns: '{makeSelection(['interactive', 'cli', 'menu'], 'make_selection')}'")
    print(f"Returns: '{makeSelection(['interactive', 'cli', 'menu'], 'make_selection', multi_select=True)}'")
