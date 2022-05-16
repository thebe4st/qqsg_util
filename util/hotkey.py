import win32con
import ctypes
import ctypes.wintypes
from ctypes import *
from threading import Thread
from time import sleep, time

from util.thead import thread_it

class Hotkey(Thread):
    user32 = ctypes.windll.user32
    hkey_list = {}
    hkey_flags = {}  # 按下
    hkey_running = {}  # 启停
    _reg_list = {}  # 待注册热键信息

    def regiskey(self, hwnd=None, flagid=0, fnkey=win32con.MOD_ALT, vkey=win32con.VK_F9):  # 注册热键，默认一个alt+F9
        return self.user32.RegisterHotKey(hwnd, flagid, fnkey, vkey)

    def get_reginfo(self):
        return self._reg_list

    def get_id(self, func):
        self_id = None
        for id in self.get_reginfo():
            if self.get_reginfo()[id]["func"] == func:
                self_id = id
                break
        if self_id:
            self.hkey_running[self_id] = True
        return self_id

    def get_running_state(self, self_id):
        if self.hkey_running.get(self_id):
            return self.hkey_running[self_id]
        else:
            return False

    def reg(self, key, func, args=None):
        id = int(str(round(time()*10))[-6:])
        fnkey = key[0]
        vkey = key[1]
        info = {
            "fnkey": fnkey,
            "vkey": vkey,
            "func": func,
            "args": args
        }
        self._reg_list[id] = info
        # print(info)  #这里待注册的信息
        sleep(0.1)
        return id

    def fast_reg(self, id, key=(0, win32con.VK_HOME), func=lambda: print('热键注册开始')):
        if not self.regiskey(None, id, key[0], key[1]):
            print("热键注册失败")
            return None
        self.hkey_list[id] = func
        self.hkey_flags[id] = False
        return id
        

        
    def callback(self):
        def inner(self=self):
            for flag in self.hkey_flags:
                self.hkey_flags[flag] = False

            while True:
                for id, func in self.hkey_list.items():
                    if self.hkey_flags[id]:
                        args = self._reg_list[id]["args"]
                        if args:
                            # print(args)   #这里打印传入给注册函数的参数
                            thread_it(func, *args)
                        else:
                            thread_it(func)
                        self.hkey_flags[id] = False
        return inner

    def run(self):
        for id in self._reg_list:
            reg_info = self._reg_list[id]
            fnkey = reg_info["fnkey"]
            vkey = reg_info["vkey"]
            func = reg_info["func"]
            self.fast_reg(id, (fnkey, vkey), func)

        fn = self.callback()
        thread_it(fn)  # 启动监听热键按下线程

        try:
            msg = ctypes.wintypes.MSG()
            while True:
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam in self.hkey_list:
                            self.hkey_flags[msg.wParam] = True
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        finally:
            for id in self.hkey_list:
                self.user32.UnregisterHotKey(None, id)

