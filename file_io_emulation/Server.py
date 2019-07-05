from dokan.Controller import Controller as dokan_controller
import dokan.dokan_structure as dokan_structure
from PythonSingleton.Singleton import Singleton as SLT
from ctypes import *
import ctypes.wintypes as wintypes
import _thread

class Server(SLT):

    def __Singleton_Init__(self):
        dokan_controller().set_options("k")
        dokan_controller().set_operations({
            "ZwCreateFile": self.ZwCreateFile_handle,
            "Cleanup": self.Cleanup_and_CloseFile_handle,
            "CloseFile": self.Cleanup_and_CloseFile_handle,
            "GetDiskFreeSpace": self.GetDiskFreeSpace_handle,
            "GetVolumeInformation": self.GetVolumeInformation_handle,
            "ReadFile": self.ReadFile_handle,
            "WriteFile": self.WriteFile_handle,
            "FindFiles": self.FindFiles_handle,
            "FindFilesWithPattern": self.FindFilesWithPattern_handle,
        })
    
    def FindFilesWithPattern_handle(self, *argus):
        print("FindFilesWithPattern_handle: " + argus[0])
        find_data = dokan_structure.WIN32_FIND_DATAW()
        argus[2](find_data, argus[3])
        return 0

    def FindFiles_handle(self, *argus):
        print("FindFiles_handle: " + argus[0])
        return 0

    def ZwCreateFile_handle(self, *argus):
        return 0
    
    def Cleanup_and_CloseFile_handle(self, *argus):
        return 0

    def GetDiskFreeSpace_handle(self, *argus):
        # print(b1.contents)
        argus[0][0] = c_ulonglong(10 * 1024 * 1024)
        argus[2][0] = c_ulonglong(10 * 1024 * 1024)
        argus[1][0] = c_ulonglong(20 * 1024 * 1024)
        # print(b3.contents)
        # b2.contents = c_ulonglong(10 * 1024 * 1024)
        # b2 = byref(c_ulonglong(10 * 1024 * 1024))
        return 0
    def GetVolumeInformation_handle(self, *argus):
        # argus[0][0] = wintypes.LPWSTR("aaaa")
        # argus[0].contents = pointer(wintypes.LPWSTR("aaaa"))
        return 0

    def ReadFile_handle(self, *argus):
        return 0

    def WriteFile_handle(self, *argus):
        return 0

    def start(self):
        """启动dokan
        """
        _thread.start_new_thread(dokan_controller().dokan_start, ())
    
    def stop(self):
        """停止dokan
        """
        dokan_controller().dokan_stop()