from ctypes import *
import ctypes.wintypes as wintypes

class DOKAN_OPTIONS(Structure):
    _fields_ = [
        ('Version', wintypes.USHORT),
        ('ThreadCount', wintypes.USHORT),
        ('Options', wintypes.ULONG),
        ('GlobalContext', c_ulonglong),
        ('MountPoint', wintypes.LPCWSTR),
        ('UNCName', wintypes.LPCWSTR),
        ('Timeout', wintypes.USHORT),
        ('AllocationUnitSize', wintypes.USHORT),
        ('SectorSize', wintypes.USHORT),
    ]

class DOKAN_FILE_INFO(Structure):
    _fields_ = [
        ('Context', c_ulonglong),
        ('DokanContext', c_ulonglong),
        ('DokanOptions', DOKAN_OPTIONS),
        ('ProcessId', wintypes.ULONG),
        ('IsDirectory', wintypes.WCHAR),
        ('DeleteOnClose', wintypes.WCHAR),
        ('PagingIo', wintypes.WCHAR),
        ('SynchronousIo', wintypes.WCHAR),
        ('Nocache', wintypes.WCHAR),
        ('WriteToEndOfFile', wintypes.WCHAR),
    ]

class DOKAN_OPERATIONS(Structure):
    _fields_ = [
        ('ZwCreateFile', WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, DOKAN_FILE_INFO)),
        ('Cleanup', WINFUNCTYPE(wintypes.LPCWSTR, DOKAN_FILE_INFO)),
        ('CloseFile', WINFUNCTYPE(wintypes.LPCWSTR, DOKAN_FILE_INFO)),
        ('ReadFile', WINFUNCTYPE(wintypes.LPCWSTR, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD, c_longlong, DOKAN_FILE_INFO)),
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