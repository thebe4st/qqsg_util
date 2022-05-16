import win32gui
import time
from util.keyboard import press

def start_output_a(func, hotkey):
    print('开始卡键')
    self_id = hotkey.get_id(func)
    handle = win32gui.GetForegroundWindow()
    while hotkey.get_running_state(self_id):
        press(handle,'a')
        time.sleep(0.3)