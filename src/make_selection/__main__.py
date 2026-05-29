import argparse
from .make_selection import *

def showcase():
    print(f"Returns: '{makeSelection(['interactive', 'cli', 'menu'], 'make_selection')}'", file=sys.stderr)
    print(f"Returns: '{makeSelection(['interactive', 'cli', 'menu'], 'make_selection', multi_select=True)}'", file=sys.stderr)

def test_keys():
    print(f"{ANSI_YELLOW}Testing keyboard interactively!{ANSI_RESET}")
    test_cases = [
        ("Press up arrow \u2191",    (KeyCode.UP, None)),
        ("Press down arrow \u2193",  (KeyCode.DOWN, None)),
        ("Press right arrow \u2192", (None, None)),
        ("Press left arrow \u2190",  (None, None)),
        ("Press enter \u21B5",       (KeyCode.SELECT, None)),
        (f"Press {multi_select_modifier_string}+\u2192", (KeyCode.SELECT_MULTI, None)),
        ("Press backspace \u232b",   (KeyCode.DELETE_CHAR, None)),
        ("Press lowercase a",        (KeyCode.SEARCHABLE, 'a')),
        ("Press uppercase A",        (KeyCode.SEARCHABLE, 'A')),
        ("Press number 7",           (KeyCode.SEARCHABLE, '7')),
        ("Press pound #",            (KeyCode.SEARCHABLE, '#')),
        ("Press ctl+c",              (KeyCode.CANCEL, None)),
    ]
    num_errors = 0
    for msg, expected in test_cases:
        print(msg, end="", flush=True)
        if getChar() == expected:
            print(" [\u2705]")
        else:
            num_errors += 1
            print(" [\u274C]")
    if num_errors == 0:
        print(f"{ANSI_GREEN}Working :){ANSI_RESET}")
    else:
        print(f"{ANSI_RED}not working :({ANSI_RESET}")

def explore():
    print("Start pressing keys to see what values are read!")
    print(f"{ANSI_YELLOW}ctl+c to exit{ANSI_RESET}")
    while True:
        key_press = readKeyPress()
        if key_press == SPECIAL_KEY:
            key_press = (key_press, readKeyPress())
        if key_press == CTL_C:
            print(f"Key pressed: {key_press} {ANSI_RED}(exit){ANSI_RESET}")
            break
        print(f"Key pressed: {key_press}")

arg_parser = argparse.ArgumentParser(description="Interactive testing.")
sub_parsers = arg_parser.add_subparsers(required=True)

arg_parser_showcase = sub_parsers.add_parser("showcase", help="Interactive example.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
arg_parser_showcase.set_defaults(func=showcase)

arg_parser_test_keys = sub_parsers.add_parser("test_keys", help="Test keyboard input.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
arg_parser_test_keys.set_defaults(func=test_keys)

arg_parser_test_keys = sub_parsers.add_parser("explore", help="Explore key presses.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
arg_parser_test_keys.set_defaults(func=explore)

args_main = arg_parser.parse_args()
args_main.func()
