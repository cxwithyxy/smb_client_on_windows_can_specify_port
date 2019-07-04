from ctypes import *
import ctypes.wintypes as wintypes
import PythonSingleton.Singleton as SLT
import sys

class DOKAN_OPTIONS(Structure):
    pass
class DOKAN_FILE_INFO(Structure):
    pass
class DOKAN_OPERATIONS(Structure):
    pass

class builder(SLT.Singleton):

    structure_class_dict = {
        "DOKAN_OPTIONS": {
            'Version': "wintypes.USHORT",
            'ThreadCount': "wintypes.USHORT",
            'Options': "wintypes.ULONG",
            'GlobalContext': "c_ulonglong",
            'MountPoint': "wintypes.LPCWSTR",
            'UNCName': "wintypes.LPCWSTR",
            'Timeout': "wintypes.USHORT",
            'AllocationUnitSize': "wintypes.USHORT",
            'SectorSize': "wintypes.USHORT",
        },
        "DOKAN_FILE_INFO": {
            'Context': "c_ulonglong",
            'DokanContext': "c_ulonglong",
            'DokanOptions': "DOKAN_OPTIONS",
            'ProcessId': "wintypes.ULONG",
            'IsDirectory': "wintypes.WCHAR",
            'DeleteOnClose': "wintypes.WCHAR",
            'PagingIo': "wintypes.WCHAR",
            'SynchronousIo': "wintypes.WCHAR",
            'Nocache': "wintypes.WCHAR",
            'WriteToEndOfFile': "wintypes.WCHAR",
        },
        "DOKAN_OPERATIONS": {
            'ZwCreateFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, DOKAN_FILE_INFO)",
            'Cleanup': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, DOKAN_FILE_INFO)",
            'CloseFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, DOKAN_FILE_INFO)",
            'ReadFile': "WINFUNCTYPE(wintypes.LPCWSTR, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD, c_longlong, DOKAN_FILE_INFO)",
            'WriteFile': "WINFUNCTYPE(c_wchar_p)",
            'FlushFileBuffers': "WINFUNCTYPE(c_wchar_p)",
            'GetFileInformation': "WINFUNCTYPE(c_wchar_p)",
            'FindFiles': "WINFUNCTYPE(c_wchar_p)",
            'FindFilesWithPattern': "WINFUNCTYPE(c_wchar_p)",
            'SetFileAttributes': "WINFUNCTYPE(c_wchar_p)",
            'SetFileTime': "WINFUNCTYPE(c_wchar_p)",
            'DeleteFile': "WINFUNCTYPE(c_wchar_p)",
            'DeleteDirectory': "WINFUNCTYPE(c_wchar_p)",
            'MoveFile': "WINFUNCTYPE(c_wchar_p)",
            'SetEndOfFile': "WINFUNCTYPE(c_wchar_p)",
            'SetAllocationSize': "WINFUNCTYPE(c_wchar_p)",
            'LockFile': "WINFUNCTYPE(c_wchar_p)",
            'UnlockFile': "WINFUNCTYPE(c_wchar_p)",
            'GetDiskFreeSpace': "WINFUNCTYPE(c_wchar_p)",
            'GetVolumeInformation': "WINFUNCTYPE(c_wchar_p)",
            'Mounted': "WINFUNCTYPE(c_wchar_p)",
            'Unmounted': "WINFUNCTYPE(c_wchar_p)",
            'GetFileSecurity': "WINFUNCTYPE(c_wchar_p)",
            'SetFileSecurity': "WINFUNCTYPE(c_wchar_p)",
            'FindStreams': "WINFUNCTYPE(c_wchar_p)",
            'FindStreams': "WINFUNCTYPE(c_wchar_p)",
        },
    }


    def __Singleton_Init__(self):
        self.init_dokan_structure_class()

    def init_dokan_structure_class(self):
        """初始化类的结构
        """
        for class_name in self.structure_class_dict:
            now_dict = self.structure_class_dict[class_name]
            now_class = getattr(sys.modules["dokan.dokan_structure"], class_name)
            now_class.class_dict = now_dict
            fields_for_set = []
            for field_name in now_dict:
                now_dict[field_name] = eval(now_dict[field_name])
                fields_for_set.append((field_name, now_dict[field_name]))
            now_class._fields_ = fields_for_set

    def build_DOKAN_OPTIONS(self):
        """构建DOKAN_OPTIONS结构体
        """
        dokan_options = DOKAN_OPTIONS()
        dokan_options.Version = 122
        # dokan_options.ThreadCount = 1
        dokan_options.Options = 32
        dokan_options.MountPoint = wintypes.LPCWSTR("K")
        # dokan_options.UNCName = c_wchar_p("")
        # dokan_options.Timeout = 5 * 1000
        dokan_options.AllocationUnitSize = 4 * 1024
        # dokan_options.SectorSize = 10 * 1024 * 1024
        return dokan_options
    
    def build_DOKAN_OPERATIONS(self):
        """构建DOKAN_OPERATIONS结构体
        """
        dokan_operations = DOKAN_OPERATIONS()
        return dokan_operations