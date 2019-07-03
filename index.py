import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from ctypes import *
import ctypes.wintypes as wintypes
import dokan.dokan_structure as dokan_structure

dokan = windll.LoadLibrary("C:\Windows\System32\dokan1.dll")
# print(a.DokanUnmount)

dokan_options = dokan_structure.DOKAN_OPTIONS()

dokan_options.Version = 122
# dokan_options.ThreadCount = 1
# dokan_options.Options = 1
dokan_options.MountPoint = wintypes.LPCWSTR("K:\\")
# dokan_options.UNCName = c_wchar_p("")
# dokan_options.Timeout = 5 * 1000
dokan_options.AllocationUnitSize = 4 * 1024
dokan_options.SectorSize = 10 * 1024 * 1024

def aaa(b1,b2,b3,b4,b5,b6,b7,b8):
    print("asdasdad")
    return 0

dokan_operations = dokan_structure.DOKAN_OPERATIONS()
dokan_operations.ZwCreateFile = dokan_structure.DOKAN_OPERATIONS._fields_[0][1](aaa)
# dokan_operations.Cleanup = WINFUNCTYPE(wintypes.LPCWSTR, dokan_structure.DOKAN_FILE_INFO)(aaa)
# dokan_operations.CloseFile = WINFUNCTYPE(wintypes.LPCWSTR, dokan_structure.DOKAN_FILE_INFO)(aaa)

print("r u n")

a = dokan.DokanMain(dokan_options, dokan_operations)

# print(a)

# dokan.DokanUnmount(c_wchar("K:/"))

input("run finish waitting for ending")