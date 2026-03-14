import subprocess
import time
import pyautogui

def open_new_tab():
    pyautogui.hotkey('win', 'd')  # minimize all windows
    pyautogui.hotkey('win', 'd')  # restore all windows
    pyautogui.hotkey('win', 'tab')  # open task view

def main():
    open_new_tab()

if __name__ == "__main__":
    main()