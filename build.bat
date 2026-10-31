
@echo off
D:
cd D:\Python\Projects\PhoneBook

pause

.venv\Scripts\python.exe -m PyInstaller main.py -w --add-data "assets;assets" --add-data "utils;utils" --add-data "models;models" --add-data "ui;ui" --add-data "core;core"

pause
