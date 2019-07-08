from dokan.Controller import Controller as dokan_controller
import dokan.dokan_structure as dokan_structure
from PythonSingleton.Singleton import Singleton as SLT
from ctypes import *
import ctypes.wintypes as wintypes
import _thread

class Server(SLT):

    files_tree = []
    volume_name = "我虚拟出来的硬盘"
    mount_point = "k"

    def __Singleton_Init__(self):
        dokan_controller().set_options(self.mount_point)
        dokan_controller().set_operations({
            "ZwCreateFile": self.ZwCreateFile_handle,
            "Cleanup": self.Cleanup_handle,
            "CloseFile": self.CloseFile_handle,
            "GetDiskFreeSpace": self.GetDiskFreeSpace_handle,
            "GetVolumeInformation": self.GetVolumeInformation_handle,
            "ReadFile": self.ReadFile_handle,
            "WriteFile": self.WriteFile_handle,
            "FindFiles": self.FindFiles_handle,
            "FindFilesWithPattern": self.FindFilesWithPattern_handle,
        })
    
    def FindFilesWithPattern_handle(self, *argus):
        print("FindFilesWithPattern_handle")
        find_data = wintypes.WIN32_FIND_DATAW()
        find_data.cFileName = ("aaaa.txt")
        find_data.cAlternateFileName = "txt"
        argus[2](pointer(find_data), argus[3])
        find_data = wintypes.WIN32_FIND_DATAW()
        find_data.cFileName = ("bbbbb.txt")
        argus[2](pointer(find_data), argus[3])
        return 0

    def FindFiles_handle(self, *argus):
        print("FindFiles_handle")
        return 0

    def ZwCreateFile_handle(self, *argus):
        # print("ZwCreateFile_handle")
        if(argus[0] != "\\"):
            # print(argus[0])
            # print(argus[1])
            # print(argus[2])
            # print(argus[3])
            # print(argus[4])
            # print(argus[5])
            # print(argus[6])
            print(argus[7].contents.IsDirectory)
            argus[7].contents.IsDirectory
        return 0
    
    def Cleanup_handle(self, *argus):
        # print("Cleanup_handle")
        return 0

    def CloseFile_handle(self, *argus):
        # print("CloseFile_handle")
        return 0

    def GetDiskFreeSpace_handle(self, *argus):
        free = 20 * 1024 * 1024
        total = 20 * 1024 * 1024
        argus[0][0] = c_ulonglong(free)
        argus[1][0] = c_ulonglong(total)
        argus[2][0] = c_ulonglong(free)
        return 0

    def GetVolumeInformation_handle(self, *argus):
        sss = wintypes.LPWSTR(self.volume_name)
        memmove(argus[0], sss, len(sss.value) * 2)
        return 0

    def ReadFile_handle(self, *argus):
        print("ReadFile_handle")
        return 0

    def WriteFile_handle(self, *argus):
        print("WriteFile_handle")
        return 0

    def start(self):
        """启动dokan
        """
        _thread.start_new_thread(dokan_controller().dokan_start, ())
    
    def stop(self):
        """停止dokan
        """
        dokan_controller().dokan_stop()