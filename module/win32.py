from ctypes import *
import win32api
import win32con
import win32process

class PROCESS_BASIC_INFORMATION(Structure):
    _fields_ = [('ExitStatus', c_ulonglong),     # 接收进程终止状态
                ('PebBaseAddress', c_ulonglong),  # 接收进程环境块地址
                ('AffinityMask', c_ulonglong),  # 接收进程关联掩码
                ('BasePriority', c_ulonglong),  # 接收进程的优先级类
                ('UniqueProcessId', c_ulonglong),  # 接收进程ID
                ('InheritedFromUniqueProcessId', c_ulonglong)]  # 接收父进程ID

class MODULEENTRY32(Structure):
    _fields_ = [('dwSize', c_long),
                ('th32ModuleID', c_long),
                ('th32ProcessID', c_long),
                ('GlblcntUsage', c_long),
                ('ProccntUsage', c_long),
                ('modBaseAddr', c_long),
                ('modBaseSize', c_long),
                ('hModule', c_void_p),
                ('szModule', c_char * 256),
                ('szExePath', c_char * 260)]

TH32CS_SNAPMODULE = 8  # CreateToolhelp32Snapshot 用到的参数
TH32CS_SNAPMODULE32 = 0x00000010
TH32CS_SNAPPROCESS = 0x00000002  # CreateToolhelp32Snapshot 用到的参数
TH32CS_SNAPHEAPLIST = 0x00000001  # CreateToolhelp32Snapshot 用到的参数
TH32CS_SNAPTHREAD = 0x00000004  # CreateToolhelp32Snapshot 用到的参数
STANDARD_RIGHTS_REQUIRED = 0x000F0000  # PROCESS_ALL_ACCESS用到的参数
SYNCHRONIZE = 0x00100000  # PROCESS_ALL_ACCESS用到的参数
PROCESS_ALL_ACCESS = (STANDARD_RIGHTS_REQUIRED |
                      SYNCHRONIZE | 0xFFF)  # OpenProcess用到的参数

# forigen function
# CreateToolhelp32Snapshot
CreateToolhelp32Snapshot = windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = c_long
CreateToolhelp32Snapshot.argtypes = [c_int, c_int]
# OpenProcess
OpenProcess = windll.kernel32.OpenProcess
OpenProcess.argtypes = [c_void_p, c_int, c_long]
OpenProcess.rettype = c_long
# GetPriorityClass
GetPriorityClass = windll.kernel32.GetPriorityClass
GetPriorityClass.argtypes = [c_void_p]
GetPriorityClass.rettype = c_long
# CloseHandle
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [c_void_p]
CloseHandle.rettype = c_int
# Module32First
Module32First = windll.kernel32.Module32First
Module32First.argtypes = [c_void_p, POINTER(MODULEENTRY32)]
Module32First.rettype = c_int
# Module32Next
Module32Next = windll.kernel32.Module32Next
Module32Next.argtypes = [c_void_p, POINTER(MODULEENTRY32)]
Module32Next.rettype = c_int
# GetLastError
GetLastError = windll.kernel32.GetLastError
GetLastError.rettype = c_long

kernel32 = windll.LoadLibrary("kernel32.dll")  # 声明kernel32
ntdll = windll.LoadLibrary("ntdll.dll")  # 声明ntdll
GetLastError = kernel32.GetLastError  # GetLastError

def get_value_by_point(pid, offsets):
    hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
    ReadProcessMemory = kernel32.ReadProcessMemory
    buff = c_ulong(get_process_addr(hProcess))
    # buff = c_ulong(get_module_addr(pid,"QQSGBase.dll"))
    count = 0
    reslut = c_int32(0)

    for offset in offsets:
        addr = c_ulong(buff.value + offset)
        if count == len(offsets) - 1:
            # 最后一次float类型读出
            ReadProcessMemory(int(hProcess), addr,
                              byref(reslut), 4, None)
            break
        else:
            ReadProcessMemory(int(hProcess), addr, byref(buff), 4, None)
        count = count + 1
    win32api.CloseHandle(hProcess)
    return reslut.value

def get_process_addr(hProcess):
    modlist = win32process.EnumProcessModules(hProcess)
    return modlist[0]

# 32位程序需要使用32位python解释器读取
def get_module_addr(ProcessId, moduleName):
    hModuleSnap = c_void_p(0)
    me32 = MODULEENTRY32()
    me32.dwSize = sizeof(MODULEENTRY32)
    hModuleSnap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, ProcessId) 
    if GetLastError() != 0:
        print("CreateToolhelp32Snapshot: %d" % hModuleSnap)
        CloseHandle(hModuleSnap)
        print("错误代码：%d" % GetLastError())
        return 'Error'
    ret = Module32First(hModuleSnap, pointer(me32))
    if GetLastError() != 0:
        print("hModuleSnap: %d" % hModuleSnap)
        CloseHandle(hModuleSnap)
        print("错误代码：%d" % GetLastError())
        return 'Error'
    else:
        if (Module32First(hModuleSnap, pointer(me32))):
            if str(me32.szModule) == moduleName:
                CloseHandle(hModuleSnap)
                return me32.modBaseAddr
            else:
                Module32Next(hModuleSnap, pointer(me32))
                while int(GetLastError()) != 18:  # 返回值18意思：(18)- 没有更多文件。
                    if str(me32.szModule,'utf-8') == moduleName:
                        CloseHandle(hModuleSnap)
                        return me32.modBaseAddr
                    else:
                        Module32Next(hModuleSnap, pointer(me32))
                CloseHandle(hModuleSnap)
                print('找不到模块名为： %s' % moduleName)
        else:
            print('Module32First 错误,返回： %s' % GetLastError())
            CloseHandle(hModuleSnap)
            