@echo off

call rmdir /s /q dist src\make_selection.egg-info
call python -m build