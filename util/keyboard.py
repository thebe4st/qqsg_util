import win32api
import win32con

import const

def press(handle,key):
    win32api.SendMessage(handle, win32con.WM_KEYDOWN, const.keyboard_map[key], 0)
    win32api.SendMessage(handle, win32con.WM_KEYUP, const.keyboard_map[key], 0)