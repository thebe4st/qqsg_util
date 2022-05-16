import win32gui
import win32process
import time

from util.keyboard import press
import const
import module.win32

NEED_BLOOD_THROLD = 2000
NEED_MAGIC_THROLD = 500

BIG_VALUE = 9999999

def get_blood(pid):
    for offsets in const.blood_offsets:
        t = module.win32.get_value_by_point(pid, offsets)
        if t > 32 and t < 100000:
            return t
    return BIG_VALUE

def get_magic(pid):
    for offsets in const.magic_offsets:
        t = module.win32.get_value_by_point(pid, offsets)
        if t > 32 and t < 100000:
            return t
    return BIG_VALUE




def start_auto_blood(func, hotkey):
    self_id = hotkey.get_id(func)
    handle = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(handle)
    print('开始自动补给,当前血量:[%d]' % get_blood(pid))
    print('开始自动补给,当前蓝量:[%d]' % get_magic(pid))
    while hotkey.get_running_state(self_id):
        current_blood = get_blood(pid)
        current_magic = get_magic(pid)
        
        if NEED_BLOOD_THROLD > current_blood:
            print('检测到当前血量[%d]低于设定的[%d],自动使用药品' %
                  (current_blood, NEED_BLOOD_THROLD))
            press(handle,'e')
            
        if NEED_MAGIC_THROLD > current_magic:
            print('检测到当前蓝量[%d]低于设定的[%d],自动使用药品' %
                  (current_magic, NEED_MAGIC_THROLD))
            press(handle,'r')
        time.sleep(0.3)