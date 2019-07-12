from dokan.Controller import Controller as dokan_controller
import dokan.dokan_structure as dokan_structure
from PythonSingleton.Singleton import Singleton as SLT
from ctypes import *
import ctypes.wintypes as wintypes
import _thread
from fs.memoryfs import MemoryFS
import dokan.ntstatus as ntstatus
import dokan.fileinfo as fileinfo
from functools import partial as currying

class Server(SLT):

    files_tree = []
    volume_name = "我虚拟出来的硬盘"
    mount_point = "k"
    mem_fs = None

    def init_files_tree(self):
        self.mem_fs = MemoryFS()
        self.mem_fs.writetext('a.txt','i am a')
        self.mem_fs.writetext('b.txt','i am b')
        self.mem_fs.makedir("cxcxcx")
        self.mem_fs.writetext('cxcxcx/aaaa.txt','i am in dir cxcxcx , i am named aaaa')
        self.mem_fs.writetext('cxcxcx/bbbbbb.txt','b1b12b2b12b2b12b12b12b12b123b123b123b23bb1211bb')
        self.mem_fs.tree()

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
            "GetFileInformation": self.GetFileInformation_handle,
            "GetFileSecurity": self.GetFileSecurity_handle
        })
        self.init_files_tree()
    
    def GetFileSecurity_handle(self, *argus):
        print("GetFileSecurity_handle")
        return ntstatus.STATUS_SUCCESS

    def GetFileInformation_handle(self, *argus):
        path = self.get_path_from_dokan_path(argus[0])
        if(not self.mem_fs.exists(path)):
            return ntstatus.STATUS_SUCCESS
        filesize = self.mem_fs.getsize(path)
        if(self.mem_fs.isfile(path)):
            argus[1].contents.dwFileAttributes = 128
        else:
            argus[2].contents.IsDirectory = c_ubyte(True)
            argus[1].contents.dwFileAttributes = 16
        argus[1].contents.ftCreationTime = wintypes.FILETIME()
        argus[1].contents.ftLastAccessTime = wintypes.FILETIME()
        argus[1].contents.ftLastWriteTime = wintypes.FILETIME()
        argus[1].contents.dwVolumeSerialNumber = wintypes.DWORD(0)
        argus[1].contents.nFileSizeHigh = wintypes.DWORD(0)
        argus[1].contents.nFileSizeLow = wintypes.DWORD(filesize)
        argus[1].contents.nNumberOfLinks = wintypes.DWORD(1)
        argus[1].contents.nFileIndexHigh = wintypes.DWORD(99)
        argus[1].contents.nFileIndexLow = wintypes.DWORD(99)
        return ntstatus.STATUS_SUCCESS

    def FindFilesWithPattern_handle(self, *argus):
        path = self.get_path_from_dokan_path(argus[0])
        # print("FindFilesWithPattern: " + path)
        for walk_path in self.mem_fs.walk.dirs(path, max_depth = 1):
            if(self.mem_fs.exists(walk_path)):
                info = self.mem_fs.getinfo(walk_path)
                find_data = wintypes.WIN32_FIND_DATAW()
                find_data.dwFileAttributes = 16
                find_data.cFileName = info.name
                argus[2](pointer(find_data), argus[3])
        for walk_path in self.mem_fs.walk.files(path, max_depth = 1):
            if(self.mem_fs.exists(walk_path)):
                info = self.mem_fs.getinfo(walk_path)
                filesize = self.mem_fs.getsize(walk_path)
                find_data = wintypes.WIN32_FIND_DATAW()
                find_data.dwFileAttributes = 128
                find_data.cFileName = info.name
                find_data.cAlternateFileName = info.suffixes[0]
                find_data.ftCreationTime = wintypes.FILETIME()
                find_data.ftLastAccessTime = wintypes.FILETIME()
                find_data.ftLastWriteTime = wintypes.FILETIME()
                find_data.nFileSizeHigh = wintypes.DWORD(0)
                find_data.nFileSizeLow = wintypes.DWORD(filesize)
                find_data.dwReserved0 = wintypes.DWORD(0)
                find_data.dwReserved1 = wintypes.DWORD(0)
                argus[2](pointer(find_data), argus[3])
        return ntstatus.STATUS_SUCCESS

    def FindFiles_handle(self, *argus):
        return ntstatus.STATUS_SUCCESS

    def get_path_from_dokan_path(self, dokan_path):
        path = str(dokan_path)
        path = path.replace("\\", "/")
        return path

    def ZwCreateFile_handle(self, *argus):
        '''
        https://docs.microsoft.com/zh-cn/windows/win32/api/winternl/nf-winternl-ntcreatefile
        '''
        print("\nZwCreateFile_handle\n")
        FileName = argus[0]
        SecurityContext = argus[1]
        DesiredAccess = argus[2]
        FileAttributes = argus[3]
        ShareAccess = argus[4]
        CreateDisposition = argus[5]
        CreateOptions = argus[6]
        path = self.get_path_from_dokan_path(FileName)
        is_file = self.mem_fs.isfile(path)
        check_is_exists = currying(self.mem_fs.exists, path)
        print(path)
        print("CreateDisposition: "+ str(hex(CreateDisposition)))
        print("CreateOptions: " + str(hex(CreateOptions)))
        print("DesiredAccess:" + str(hex(DesiredAccess)))
        if(CreateDisposition == fileinfo.CREATE_NEW):
            if(check_is_exists()):
                if(is_file):
                    argus[7].contents.IsDirectory = c_ubyte(False)
                else:
                    argus[7].contents.IsDirectory = c_ubyte(True)
                return ntstatus.STATUS_SUCCESS
            return ntstatus.STATUS_OBJECT_NAME_NOT_FOUND
        if(CreateDisposition == fileinfo.CREATE_ALWAYS):
            if(CreateOptions & fileinfo.FILE_DIRECTORY_FILE):
                if(check_is_exists()):
                    return ntstatus.STATUS_OBJECT_NAME_COLLISION
                self.mem_fs.makedir(path)
                self.mem_fs.tree()
                return ntstatus.STATUS_SUCCESS
            if(CreateOptions & fileinfo.FILE_NON_DIRECTORY_FILE):
                pass

    
    def Cleanup_handle(self, *argus):
        # print("Cleanup_handle")
        return ntstatus.STATUS_SUCCESS

    def CloseFile_handle(self, *argus):
        # print("CloseFile_handle")
        return ntstatus.STATUS_SUCCESS

    def GetDiskFreeSpace_handle(self, *argus):
        # print("GetDiskFreeSpace_handle")
        free = 20 * 1024 * 1024
        total = 20 * 1024 * 1024
        argus[0][0] = c_ulonglong(free)
        argus[1][0] = c_ulonglong(total)
        argus[2][0] = c_ulonglong(free)
        return ntstatus.STATUS_SUCCESS

    def GetVolumeInformation_handle(self, *argus):
        # print("GetVolumeInformation_handle")
        sss = wintypes.LPWSTR(self.volume_name)
        memmove(argus[0], sss, len(sss.value) * 2)
        return ntstatus.STATUS_SUCCESS

    def ReadFile_handle(self, *argus):
        file_path = self.get_path_from_dokan_path(argus[0])
        buffer = argus[1].contents
        buffer_len = argus[2]
        read_len_buffer = argus[3]
        offset = argus[4]
        if(self.mem_fs.exists(file_path)):
            filesize = self.mem_fs.getsize(file_path)
            if(argus[4] >= filesize):
                return ntstatus.STATUS_SUCCESS
            f = self.mem_fs.open(file_path, "rb")
            f.seek(offset, 0)
            read_out = f.read(buffer_len)
            sss = create_string_buffer(read_out)
            memmove(buffer, sss, len(sss.value))
            memmove(read_len_buffer, pointer(c_ulong(len(sss.value))), sizeof(c_ulong))
        return ntstatus.STATUS_SUCCESS

    def WriteFile_handle(self, *argus):
        # print("WriteFile_handle")
        return ntstatus.STATUS_SUCCESS

    def start(self):
        """启动dokan
        """
        _thread.start_new_thread(dokan_controller().dokan_start, ())
    
    def stop(self):
        """停止dokan
        """
        dokan_controller().dokan_stop()