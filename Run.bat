@echo off
.python_embed\python.exe -m pip install curses
pause


mode con: cols=150 lines=50
".python_embed\python.exe" main.py
pause