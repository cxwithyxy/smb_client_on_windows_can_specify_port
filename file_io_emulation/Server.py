from dokan.Controller import Controller as dokan_controller
import dokan.dokan_structure as dokan_structure
from PythonSingleton.Singleton import Singleton as SLT
from ctypes import *
import ctypes.wintypes as wintypes
import _thread
from fs.memoryfs import MemoryFS
from file_io_emulation.File import File

class Server(SLT):

    files_tree = []
    volume_name = "我虚拟出来的硬盘"
    mount_point = "k"
    mem_fs = None

    def init_files_tree(self):
        self.mem_fs = MemoryFS()
        self.mem_fs.writetext('a.txt','i am a')
        self.mem_fs.writetext('b.txt','i am b')


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
            "GetFileInformation": self.GetFileInformation_handle
        })
        self.init_files_tree()
    
    def GetFileInformation_handle(self, *argus):
        if(self.mem_fs.isfile(self.get_path_from_dokan_path(argus[0]))):
            argus[1].contents.dwFileAttributes = 128
        else:
            argus[2].contents.IsDirectory = c_ubyte(True)
            argus[1].contents.dwFileAttributes = 16
        return 0x00000000

    def FindFilesWithPattern_handle(self, *argus):
        for path in self.mem_fs.walk.files():
            info = self.mem_fs.getinfo(path)
            find_data = wintypes.WIN32_FIND_DATAW()
            find_data.cFileName = info.name
            find_data.cAlternateFileName = info.suffixes[0]
            argus[2](pointer(find_data), argus[3])
        return 0

    def FindFiles_handle(self, *argus):
        # print("FindFiles_handle")
        return 0

    def get_path_from_dokan_path(self, dokan_path):
        path = str(dokan_path)
        path = path.replace("\\", "/")
        return path

    def ZwCreateFile_handle(self, *argus):
        # print("ZwCreateFile_handle")
        if(self.mem_fs.isfile(self.get_path_from_dokan_path(argus[0]))):
            # print(argus[7].contents.IsDirectory)
            # argus[7].contents.Context = 6727
            return 0xC0000035
        # else:
        #     print("FileName")
        #     print(argus[0])
        #     print("SecurityContext")
        #     print(argus[1])
        #     print("DesiredAccess")
        #     print(argus[2])
        #     print("FileAttributes")
        #     print(argus[3])
        #     print("ShareAccess")
        #     print(argus[4])
        #     print("CreateDisposition")
        #     print(argus[5])
        #     print("CreateOptions")
        #     print(argus[6])
        #     print(argus[7].contents.IsDirectory)
        #     argus[7].contents.IsDirectory = c_ubyte(True)
        return 0
    
    def Cleanup_handle(self, *argus):
        # print("Cleanup_handle")
        return 0

    def CloseFile_handle(self, *argus):
        # print("CloseFile_handle")
        return 0

    def GetDiskFreeSpace_handle(self, *argus):
        # print("GetDiskFreeSpace_handle")
        free = 20 * 1024 * 1024
        total = 20 * 1024 * 1024
        argus[0][0] = c_ulonglong(free)
        argus[1][0] = c_ulonglong(total)
        argus[2][0] = c_ulonglong(free)
        return 0

    def GetVolumeInformation_handle(self, *argus):
        # print("GetVolumeInformation_handle")
        sss = wintypes.LPWSTR(self.volume_name)
        memmove(argus[0], sss, len(sss.value) * 2)
        return 0

    def ReadFile_handle(self, *argus):
        # print("ReadFile_handle")
        file_path = argus[0]
        buffer = argus[1].contents
        buffer_len = argus[2]
        read_len_buffer = argus[3]
        offset = argus[4]
        filesize = len(self.bbbbtxt)
        if(argus[4] >= filesize):
            return 0
        sss = create_string_buffer(self.bbbbtxt[offset:offset + buffer_len])
        memmove(buffer, sss, len(sss.value))
        memmove(read_len_buffer, pointer(c_ulong(len(sss.value))), sizeof(c_ulong))
        return 0

    def WriteFile_handle(self, *argus):
        # print("WriteFile_handle")
        return 0

    def start(self):
        """启动dokan
        """
        _thread.start_new_thread(dokan_controller().dokan_start, ())
    
    def stop(self):
        """停止dokan
        """
        dokan_controller().dokan_stop()