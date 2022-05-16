# -*- coding: utf-8 -*-

import win32con

from util.hotkey import Hotkey
from const import *
import module.win32
import module.pressa
import module.auto_blood







def print_help_msg():
    print('''
        F5 开启卡键A
        F6 关闭卡键A
        F7 开启自动补给
        F9 关闭自动补给
    ''')
    
def regist_hotkey(hotkey):
    # 注册卡键
    start_id_a = hotkey.reg(key=(0, win32con.VK_F5),
                            func=module.pressa.start_output_a, args=(module.pressa.start_output_a, hotkey))
    hotkey.reg(key=(0, win32con.VK_F6), func=stop_task,
               args=(start_id_a, hotkey))

    # 注册自动补给
    start_id_auto_blood = hotkey.reg(
        key=(0, win32con.VK_F7), func=module.auto_blood.start_auto_blood, args=(module.auto_blood.start_auto_blood, hotkey))
    hotkey.reg(key=(0, win32con.VK_F9), func=stop_task,
               args=(start_id_auto_blood, hotkey))

def stop_task(start_id, hotkey):
    hotkey.hkey_running[start_id] = False
    print('停止成功~')

def main():
    print_help_msg()
    
    hotkey = Hotkey()
    regist_hotkey(hotkey)
    hotkey.start()

if __name__ == "__main__":
    main()
