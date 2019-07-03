import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from ctypes import *

dokan = windll.LoadLibrary("C:\Windows\System32\dokan1.dll")
# print(a.DokanUnmount)

class DOKAN_OPTIONS(Structure):
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

dokan_options = DOKAN_OPTIONS()

dokan_options.Version = 122
# dokan_options.ThreadCount = 1
# dokan_options.Options = 1
dokan_options.MountPoint = c_wchar_p("K:\\")
# dokan_options.UNCName = c_wchar_p("")
# dokan_options.Timeout = 5 * 1000
# dokan_options.AllocationUnitSize = 10 * 1024 * 1024
# dokan_options.SectorSize = 10 * 1024 * 1024

class DOKAN_OPERATIONS(Structure):
    _fields_ = [
        ('ZwCreateFile', WINFUNCTYPE(c_wchar_p)),
        ('Cleanup', WINFUNCTYPE(c_wchar_p)),
        ('CloseFile', WINFUNCTYPE(c_wchar_p)),
        ('ReadFile', WINFUNCTYPE(c_wchar_p)),
        ('WriteFile', WINFUNCTYPE(c_wchar_p)),
        ('FlushFileBuffers', WINFUNCTYPE(c_wchar_p)),
        ('GetFileInformation', WINFUNCTYPE(c_wchar_p)),
        ('FindFiles', WINFUNCTYPE(c_wchar_p)),
        ('FindFilesWithPattern', WINFUNCTYPE(c_wchar_p)),
        ('SetFileAttributes', WINFUNCTYPE(c_wchar_p)),
        ('SetFileTime', WINFUNCTYPE(c_wchar_p)),
        ('DeleteFile', WINFUNCTYPE(c_wchar_p)),
        ('DeleteDirectory', WINFUNCTYPE(c_wchar_p)),
        ('MoveFile', WINFUNCTYPE(c_wchar_p)),
        ('SetEndOfFile', WINFUNCTYPE(c_wchar_p)),
        ('SetAllocationSize', WINFUNCTYPE(c_wchar_p)),
        ('LockFile', WINFUNCTYPE(c_wchar_p)),
        ('UnlockFile', WINFUNCTYPE(c_wchar_p)),
        ('GetDiskFreeSpace', WINFUNCTYPE(c_wchar_p)),
        ('GetVolumeInformation', WINFUNCTYPE(c_wchar_p)),
        ('Mounted', WINFUNCTYPE(c_wchar_p)),
        ('Unmounted', WINFUNCTYPE(c_wchar_p)),
        ('GetFileSecurity', WINFUNCTYPE(c_wchar_p)),
        ('SetFileSecurity', WINFUNCTYPE(c_wchar_p)),
        ('FindStreams', WINFUNCTYPE(c_wchar_p)),
        ('FindStreams', WINFUNCTYPE(c_wchar_p))
    ]

dokan_operations = DOKAN_OPERATIONS()

print("r u n")

a = dokan.DokanMain(dokan_options, dokan_operations)

print(a)

# dokan.DokanUnmount(c_wchar("K:/"))