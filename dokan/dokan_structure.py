from ctypes import *
import ctypes.wintypes as wintypes
import PythonSingleton.Singleton as SLT
import sys

class DOKAN_OPTIONS(Structure):
    pass
class BY_HANDLE_FILE_INFORMATION(Structure):
    pass
class DOKAN_FILE_INFO(Structure):
    pass
class DOKAN_OPERATIONS(Structure):
    pass
class FILETIME(Structure):
    pass
class UNICODE_STRING(Structure):
    pass
class DOKAN_ACCESS_STATE(Structure):
    pass
class DOKAN_IO_SECURITY_CONTEXT(Structure):
    pass
class other_func(Structure):
    pass

class Builder(SLT.Singleton):

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
        "BY_HANDLE_FILE_INFORMATION": {
            "dwFileAttributes": "wintypes.DWORD",
            "ftCreationTime": "wintypes.FILETIME",
            "ftLastAccessTime": "wintypes.FILETIME",
            "ftLastWriteTime": "wintypes.FILETIME",
            "dwVolumeSerialNumber": "wintypes.DWORD",
            "nFileSizeHigh": "wintypes.DWORD",
            "nFileSizeLow": "wintypes.DWORD",
            "nNumberOfLinks": "wintypes.DWORD",
            "nFileIndexHigh": "wintypes.DWORD",
            "nFileIndexLow": "wintypes.DWORD",
        },
        "DOKAN_FILE_INFO": {
            'Context': "c_ulonglong",
            'DokanContext': "c_ulonglong",
            'DokanOptions': "POINTER(DOKAN_OPTIONS)",
            'ProcessId': "wintypes.ULONG",
            'IsDirectory': "c_ubyte",
            'DeleteOnClose': "c_ubyte",
            'PagingIo': "c_ubyte",
            'SynchronousIo': "c_ubyte",
            'Nocache': "c_ubyte",
            'WriteToEndOfFile': "c_ubyte",
        },
        "UNICODE_STRING": {
            "Length": "wintypes.USHORT",
            "MaximumLength": "wintypes.USHORT",
            "Buffer": "c_wchar_p",
        },
        "DOKAN_ACCESS_STATE": {
            "SecurityEvaluated": "wintypes.BOOLEAN",
            "GenerateAudit": "wintypes.BOOLEAN",
            "GenerateOnClose": "wintypes.BOOLEAN",
            "AuditPrivileges": "wintypes.BOOLEAN",
            "Flags": "wintypes.ULONG",
            "RemainingDesiredAccess": "wintypes.DWORD",
            "PreviouslyGrantedAccess": "wintypes.DWORD",
            "OriginalDesiredAccess": "wintypes.DWORD",
            "SecurityDescriptor": "c_void_p",
            "ObjectName": "UNICODE_STRING",
            "ObjectType": "UNICODE_STRING",
        },
        "DOKAN_IO_SECURITY_CONTEXT": {
            "AccessState": "DOKAN_ACCESS_STATE",
            "DesiredAccess": "wintypes.DWORD",
        },
        "other_func": {
            "callback_FillFindData": "WINFUNCTYPE(c_int, wintypes.PWIN32_FIND_DATAW, POINTER(DOKAN_FILE_INFO))"
        },
        "DOKAN_OPERATIONS": {
            'ZwCreateFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR,POINTER(DOKAN_IO_SECURITY_CONTEXT), wintypes.DWORD, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, POINTER(DOKAN_FILE_INFO))",
            'Cleanup': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(DOKAN_FILE_INFO))",
            'CloseFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(DOKAN_FILE_INFO))",
            'ReadFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(c_char * 1), wintypes.DWORD, wintypes.LPDWORD, c_longlong, POINTER(DOKAN_FILE_INFO))",
            'WriteFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(c_char * 1), wintypes.DWORD, wintypes.LPDWORD, c_longlong, POINTER(DOKAN_FILE_INFO))",
            'FlushFileBuffers': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(DOKAN_FILE_INFO))",
            'GetFileInformation': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(BY_HANDLE_FILE_INFORMATION), POINTER(DOKAN_FILE_INFO))",
            'FindFiles': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, other_func.class_dict['callback_FillFindData'], POINTER(DOKAN_FILE_INFO))",
            'FindFilesWithPattern': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, wintypes.LPCWSTR, other_func.class_dict['callback_FillFindData'], POINTER(DOKAN_FILE_INFO))",
            'SetFileAttributes': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'SetFileTime': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'DeleteFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(DOKAN_FILE_INFO))",
            'DeleteDirectory': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, POINTER(DOKAN_FILE_INFO))",
            'MoveFile': "WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.BOOL, POINTER(DOKAN_FILE_INFO))",
            'SetEndOfFile': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'SetAllocationSize': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'LockFile': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'UnlockFile': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'GetDiskFreeSpace': "WINFUNCTYPE(wintypes.ULONG, POINTER(c_ulonglong), POINTER(c_ulonglong), POINTER(c_ulonglong), POINTER(DOKAN_FILE_INFO))",
            'GetVolumeInformation': "WINFUNCTYPE(wintypes.ULONG, POINTER(wintypes.LPWSTR), wintypes.DWORD, wintypes.LPDWORD, wintypes.LPDWORD, wintypes.LPDWORD, wintypes.LPWSTR, wintypes.DWORD, POINTER(DOKAN_FILE_INFO))",
            'Mounted': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'Unmounted': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'GetFileSecurity': 'WINFUNCTYPE(wintypes.ULONG, wintypes.LPCWSTR, wintypes.DWORD, c_void_p, wintypes.ULONG, POINTER(wintypes.ULONG), POINTER(DOKAN_FILE_INFO))',
            'SetFileSecurity': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
            'FindStreams': "WINFUNCTYPE(wintypes.ULONG, c_wchar_p)",
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
                try:
                    now_dict[field_name] = eval(now_dict[field_name])
                except BaseException as e:
                    print(e)
                    print("ERROR===== " + field_name + "=====")
                fields_for_set.append((field_name, now_dict[field_name]))
            now_class._fields_ = fields_for_set

    def build_DOKAN_OPTIONS(self, mount_point):
        """构建DOKAN_OPTIONS结构体

        Args:
            
            mount_point: 挂载点, 如k, 代表挂载成k盘
        """
        dokan_options = DOKAN_OPTIONS()
        dokan_options.Version = 122
        dokan_options.ThreadCount = wintypes.USHORT(1)
        # dokan_options.Options = 32
        dokan_options.MountPoint = wintypes.LPCWSTR(mount_point)
        # dokan_options.UNCName = c_wchar_p("")
        # dokan_options.Timeout = 5 * 1000
        # dokan_options.AllocationUnitSize = 4 * 1024
        # dokan_options.SectorSize = 10 * 1024 * 1024
        return dokan_options
    
    def build_DOKAN_OPERATIONS(self, callback_dict = {}):
        """构建DOKAN_OPERATIONS结构体

        Args:

            callback_dict: 回调函数字典，对应在dokan.h中DOKAN_OPERATIONS结构体的函数及其名称
        """
        dokan_operations = DOKAN_OPERATIONS()
        for i in callback_dict:
            setattr(dokan_operations, i, dokan_operations.class_dict[i](callback_dict[i]))
        return dokan_operations