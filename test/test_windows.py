import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src/make_selection")

import unittest
import win32_mappings
from key_codes import KeyCode
from unittest.mock import patch, MagicMock


class TestWindowsMappings(unittest.TestCase):
    @patch("msvcrt.getch")
    def test_up(self, getch_mock: MagicMock):
        getch_mock.side_effect = [chr(win32_mappings.SPECIAL_KEY), chr(win32_mappings.ARROW_UP)]
        key_code, char = win32_mappings.getChar()
        self.assertEqual(key_code, KeyCode.UP)
        self.assertEqual(char, None)

    @patch("msvcrt.getch")
    def test_down(self, getch_mock: MagicMock):
        getch_mock.side_effect = [chr(win32_mappings.SPECIAL_KEY), chr(win32_mappings.ARROW_DOWN)]
        key_code, char = win32_mappings.getChar()
        self.assertEqual(key_code, KeyCode.DOWN)
        self.assertEqual(char, None)

    @patch("msvcrt.getch", return_value=chr(win32_mappings.ENTER))
    def test_select(self, getch_mock: MagicMock):
        key_code, char = win32_mappings.getChar()
        self.assertEqual(key_code, KeyCode.SELECT)
        self.assertEqual(char, None)

    @patch("msvcrt.getch", return_value=chr(win32_mappings.TAB))
    def test_select_multi(self, getch_mock: MagicMock):
        key_code, char = win32_mappings.getChar()
        self.assertEqual(key_code, KeyCode.SELECT_MULTI)
        self.assertEqual(char, None)

    @patch("msvcrt.getch", return_value=chr(win32_mappings.CTL_C))
    def test_cancel(self, getch_mock: MagicMock):
        key_code, char = win32_mappings.getChar()
        self.assertEqual(key_code, KeyCode.CANCEL)
        self.assertEqual(char, None)

    @patch("msvcrt.getch", return_value=chr(win32_mappings.BACKSPACE))
    def test_delete_char(self, getch_mock: MagicMock):
        key_code, char = win32_mappings.getChar()
        self.assertEqual(key_code, KeyCode.DELETE_CHAR)
        self.assertEqual(char, None)


    @patch("msvcrt.getch")
    def test_searchables(self, getch_mock: MagicMock):
        test_cases = [chr(i) for i in range(32, 127)]
        for expected_char in test_cases:
            getch_mock.return_value = expected_char
            with self.subTest(value=expected_char):
                key_code, char = win32_mappings.getChar()
                self.assertEqual(key_code, KeyCode.SEARCHABLE)
                self.assertEqual(char, expected_char)

if __name__ == '__main__':
    unittest.main()
