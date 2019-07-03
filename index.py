import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from ctypes import *

dokan = windll.LoadLibrary("C:\Windows\System32\dokan1.dll")
# print(a.DokanUnmount)

class Dokan_options(Structure):
    _fields_ = [
        ('Version', c_ushort),
        ('ThreadCount', c_ushort),
        ('Options', c_ulong),
        ('GlobalContext', c_ulonglong),
        ('MountPoint', c_wchar_p),
        ('UNCName', c_wchar_p),
        ('Timeout', c_ulong),
        ('AllocationUnitSize', c_ulong),
        ('SectorSize', c_ulong),
    ]

dokan_options = Dokan_options()

dokan_options.Version = 122
dokan_options.ThreadCount = 1
dokan_options.Options = 32
dokan_options.MountPoint = c_wchar_p("O:/")
dokan_options.UNCName = c_wchar_p("")
# dokan_options.Timeout = 5 * 1000
# dokan_options.AllocationUnitSize = 10 * 1024 * 1024
# dokan_options.SectorSize = 10 * 1024 * 1024

print("r u n")

a = dokan.DokanMain(dokan_options)

print(a)

dokan.DokanUnmount(c_wchar("O:/"))