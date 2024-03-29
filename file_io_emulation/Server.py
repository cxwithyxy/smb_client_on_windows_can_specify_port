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
import time
from my_lib.Config_controller.Config_controller import Config_controller as ConfC
from fs.smbfs import smbfs
import threading
from file_io_emulation.Smb_client import Smb_client

class Server(SLT):

    volume_name = ""
    mount_point = ""
    thread_count = 1
    server_fs: Smb_client
    conf: ConfC

    def get_fs(self, callback):
        self.server_fs.get_fs(callback)

    def init_files_tree(self):
        self.server_fs = Smb_client()

        # self.server_fs = MemoryFS()
        # self.get_fs().writetext('aaaattttttasdaa.txt','i am a')
        # self.get_fs().writetext('b.txt','i am b')
        # self.get_fs().makedir("cxcxcx")
        # self.get_fs().writetext('cxcxcx/aaaa.txt','i am in dir cxcxcx , i am named aaaa')
        # bbbb = ""
        # for i in range(262144):
        #     bbbb += str("ab")
        #     pass
        # bbbb += "\n====== end =====\n"
        # self.get_fs().writetext('cxcxcx/bbbb.txt',bbbb)
        # self.get_fs().makedir("qqq")
        # self.get_fs().writetext('qqq/qqq.txt','qqq')

    def operations_wrapper(func):
        def wrapper(self, *argus):
            return_value = None
            def dodo():
                nonlocal return_value
                return_value = func(self, *argus)
            t = threading.Thread(
                target = dodo,
                daemon = True
            )
            t.start()
            t.join()
            return return_value
        return wrapper

    def conf_init(self):
        self.conf = ConfC('setting.ini')
        self.conf.cd("disk")
        self.volume_name = self.conf.get('volume_name')
        self.mount_point = self.conf.get('mount_point')
        self.conf.cd("smb")
        self.thread_count = int(self.conf.get("thread"))

    def __Singleton_Init__(self):
        self.conf_init()
        
        dokan_controller().set_options(self.mount_point, self.thread_count)
        dokan_controller().set_operations({
            "ZwCreateFile": self.ZwCreateFile_handle,
            "Cleanup": self.Cleanup_handle,
            "CloseFile": self.CloseFile_handle,
            "GetDiskFreeSpace": self.GetDiskFreeSpace_handle,
            "GetVolumeInformation": self.GetVolumeInformation_handle,
            "ReadFile": self.ReadFile_handle,
            "WriteFile": self.WriteFile_handle,
            "FindFiles": self.FindFiles_handle,
            "GetFileInformation": self.GetFileInformation_handle,
            "GetFileSecurity": self.GetFileSecurity_handle,
            "MoveFile": self.MoveFile_handle,
            "DeleteFile": self.DeleteFile_handle,
            "DeleteDirectory": self.DeleteFile_handle,
            "FlushFileBuffers": self.FlushFileBuffers_handle,
            "SetAllocationSize": self.SetAllocationSize_handle
        })
        self.init_files_tree()

    def SetAllocationSize_handle(self, *argus):
        # print("\n===== SetAllocationSize_handle =====\n")
        return ntstatus.STATUS_SUCCESS

    def FlushFileBuffers_handle(self, *argus):
        # print("\n===== FlushFileBuffers_handle =====\n")
        return ntstatus.STATUS_SUCCESS

    def path_is_exists(self, path: str):
        is_exists = None
        def callback(smb_fs: smbfs.SMBFS):
            nonlocal is_exists
            is_exists = smb_fs.exists(path)
        self.get_fs(callback)
        return is_exists

    def path_is_file(self, path: str):
        is_file = None
        def callback(smb_fs: smbfs.SMBFS):
            nonlocal is_file
            is_file = smb_fs.isfile(path)
        self.get_fs(callback)
        return is_file

    def path_is_empty(self, path: str):
        isempty = None
        def callback(smb_fs: smbfs.SMBFS):
            nonlocal isempty
            isempty = smb_fs.isempty(path)
        self.get_fs(callback)
        return isempty

    @operations_wrapper
    def DeleteFile_handle(self, *argus):
        # print("DeleteFile_handle")
        # print(argus[0])
        file_path = self.get_path_from_dokan_path(argus[0])
        is_file = self.path_is_file(file_path)
        if(argus[1].contents.DeleteOnClose):
            # print(file_path)
            # print(argus[1].contents.DeleteOnClose)
            if(not is_file):
                if(not self.path_is_empty(file_path)):
                    return ntstatus.STATUS_DIRECTORY_NOT_EMPTY
        return ntstatus.STATUS_SUCCESS

    @operations_wrapper
    def MoveFile_handle(self, *argus):
        src_path = self.get_path_from_dokan_path(argus[0])
        dst_path = self.get_path_from_dokan_path(argus[1])
        # print("\n===== MoveFile_handle =====\n")
        # print(f"src_path: {src_path}")
        # print(f"dst_path: {dst_path}")
        is_exists = self.path_is_exists(src_path)
        is_file = self.path_is_file(src_path)

        if(not is_exists):
            return ntstatus.STATUS_OBJECTID_NOT_FOUND
        
        def callback(smb_fs: smbfs.SMBFS):
            nonlocal is_file
            if(is_file):
                smb_fs.move(src_path, dst_path, argus[2])
            else:
                smb_fs.movedir(src_path, dst_path, True)
        self.get_fs(callback)
        
        return ntstatus.STATUS_SUCCESS

    def GetFileSecurity_handle(self, *argus):
        # print("GetFileSecurity_handle")
        # print(argus[0])
        return ntstatus.STATUS_NOT_IMPLEMENTED

    @operations_wrapper
    def GetFileInformation_handle(self, *argus):
        path = self.get_path_from_dokan_path(argus[0])
        # print("GetFileInformation_handle")
        # print(path)
        if(not self.path_is_exists(path)):
            return ntstatus.STATUS_SUCCESS
        filesize = None
        def callback(smb_fs: smbfs.SMBFS):
            nonlocal filesize
            filesize = smb_fs.getsize(path)
        self.get_fs(callback)
        if(self.path_is_file(path)):
            argus[1].contents.dwFileAttributes = wintypes.DWORD(32)
        else:
            argus[2].contents.IsDirectory = c_ubyte(True)
            argus[1].contents.dwFileAttributes = wintypes.DWORD(16)
        argus[1].contents.ftCreationTime = wintypes.FILETIME()
        argus[1].contents.ftLastAccessTime = wintypes.FILETIME()
        argus[1].contents.ftLastWriteTime = wintypes.FILETIME()
        argus[1].contents.nFileSizeHigh = wintypes.DWORD(0)
        argus[1].contents.nFileSizeLow = wintypes.DWORD(filesize)
        return ntstatus.STATUS_SUCCESS

    @operations_wrapper
    def FindFiles_handle(self, *argus):
        path = self.get_path_from_dokan_path(argus[0])
        # print("\n===== FindFiles_handle =====\n")
        # print("FindFilesWithPattern: " + path)
        if(not self.path_is_exists(path)):
            return ntstatus.STATUS_OBJECTID_NOT_FOUND
        def callback(smb_fs: smbfs.SMBFS):
            for walk_path in smb_fs.walk.dirs(path, max_depth = 1):
                if(smb_fs.exists(walk_path)):
                    info = smb_fs.getinfo(walk_path)
                    find_data = wintypes.WIN32_FIND_DATAW()
                    find_data.dwFileAttributes = 16
                    find_data.cFileName = info.name
                    argus[1](pointer(find_data), argus[2])
            for walk_path in smb_fs.walk.files(path, max_depth = 1):
                if(smb_fs.exists(walk_path)):
                    info = smb_fs.getinfo(walk_path)
                    filesize = smb_fs.getsize(walk_path)
                    find_data = wintypes.WIN32_FIND_DATAW()
                    find_data.dwFileAttributes = 32
                    find_data.cFileName = info.name
                    if(len(info.name) >= 11):
                        info_cut = info.name.split(".")
                        cAlternateFileName = info_cut[0][0:6] + "~1." + info.suffix[0:3]
                    else:
                        find_data.cAlternateFileName = info.name
                    find_data.ftCreationTime = wintypes.FILETIME()
                    find_data.ftLastAccessTime = wintypes.FILETIME()
                    find_data.ftLastWriteTime = wintypes.FILETIME()
                    find_data.nFileSizeHigh = wintypes.DWORD(0)
                    find_data.nFileSizeLow = wintypes.DWORD(filesize)
                    find_data.dwReserved0 = wintypes.DWORD(0)
                    find_data.dwReserved1 = wintypes.DWORD(0)
                    argus[1](pointer(find_data), argus[2])
        self.get_fs(callback)
        return ntstatus.STATUS_SUCCESS

    def get_path_from_dokan_path(self, dokan_path):
        path = str(dokan_path)
        path = path.replace("\\", "/")
        return path
    
    @operations_wrapper
    def ZwCreateFile_handle(self, *argus):
        '''
        https://docs.microsoft.com/zh-cn/windows/win32/api/winternl/nf-winternl-ntcreatefile
        '''
        FileName = argus[0]
        SecurityContext = argus[1]
        DesiredAccess = argus[2]
        FileAttributes = argus[3]
        ShareAccess = argus[4]
        CreateDisposition = argus[5]
        CreateOptions = argus[6]
        DokanFileInfo = argus[7].contents
        
        DokanMapKernelToUserCreateFileFlags = dokan_controller().dokan_dll.DokanMapKernelToUserCreateFileFlags
        outDesiredAccess = wintypes.DWORD()
        outFileAttributesAndFlags = wintypes.DWORD()
        outCreationDisposition = wintypes.DWORD()
        DokanMapKernelToUserCreateFileFlags(
            DesiredAccess,
            FileAttributes,
            CreateOptions,
            CreateDisposition,
            pointer(outDesiredAccess),
            pointer(outFileAttributesAndFlags),
            pointer(outCreationDisposition)
        )
        t_DesiredAccess = outDesiredAccess.value
        t_FileAttributesAndFlags = outFileAttributesAndFlags.value
        t_CreationDisposition = outCreationDisposition.value

        path = self.get_path_from_dokan_path(FileName)
        is_file = self.path_is_file(path)
        check_is_exists = currying(self.path_is_exists, path)

        def print_out():
            print(f"\n{time.strftime('%H:%M:%S', time.localtime())}===== ZwCreateFile_handle =====\n")
            print(f"path: {path}")
            # print("CreateDisposition: "+ str(hex(CreateDisposition)))
            # print("CreateOptions: " + str(hex(CreateOptions)))
            # print("DesiredAccess:" + str(hex(DesiredAccess)))
            # print("FileAttributes:" + str(hex(FileAttributes)))
            print(f"is dir: {DokanFileInfo.IsDirectory}")
            print(f"t_CreationDisposition: {str(hex(t_CreationDisposition))}")
            print(f"t_DesiredAccess: {str(hex(t_DesiredAccess))}")
            print(f"t_FileAttributesAndFlags: {str(hex(t_FileAttributesAndFlags))}")
        # print_out()
        if(t_CreationDisposition == fileinfo.OPEN_EXISTING):
            if(check_is_exists()):
                if(is_file):
                    DokanFileInfo.IsDirectory = c_ubyte(False)
                    # DokanFileInfo.WriteToEndOfFile = c_ubyte(True)
                    # DokanFileInfo.Context = c_ulonglong(6727)
                    # print(DokanFileInfo.Context)
                    # print(DokanFileInfo.WriteToEndOfFile)
                else:
                    DokanFileInfo.IsDirectory = c_ubyte(True)
                return ntstatus.STATUS_SUCCESS
            return ntstatus.STATUS_OBJECT_NAME_NOT_FOUND
        if(
            t_CreationDisposition == fileinfo.CREATE_NEW
            or t_CreationDisposition == fileinfo.OPEN_ALWAYS
        ):
            if(CreateOptions & fileinfo.FILE_DIRECTORY_FILE):
                if(check_is_exists()):
                    return ntstatus.STATUS_OBJECT_NAME_COLLISION
                def callback(smb_fs: smbfs.SMBFS):
                    smb_fs.makedir(path)
                self.get_fs(callback)
            if(CreateOptions & fileinfo.FILE_NON_DIRECTORY_FILE):
                if(check_is_exists()):
                    return ntstatus.STATUS_OBJECT_NAME_COLLISION
                def callback2(smb_fs: smbfs.SMBFS):
                    smb_fs.create(path)
                self.get_fs(callback2)
            
            return ntstatus.STATUS_SUCCESS
        if(t_CreationDisposition == fileinfo.CREATE_ALWAYS):
            return ntstatus.STATUS_SUCCESS
        if(t_CreationDisposition == fileinfo.TRUNCATE_EXISTING):
            return ntstatus.STATUS_SUCCESS
    
    @operations_wrapper
    def Cleanup_handle(self, *argus):
        file_path = self.get_path_from_dokan_path(argus[0])
        is_file = self.path_is_file(file_path)
        if(argus[1].contents.DeleteOnClose):
            # print(file_path)
            # print(argus[1].contents.DeleteOnClose)
            if(is_file):
                def callback(smb_fs: smbfs.SMBFS):
                    smb_fs.remove(file_path)
                self.get_fs(callback)
            else:
                if(not self.path_is_empty(file_path)):
                    return ntstatus.STATUS_DIRECTORY_NOT_EMPTY
                def callback2(smb_fs: smbfs.SMBFS):
                    smb_fs.removedir(file_path)
                self.get_fs(callback2)
        return ntstatus.STATUS_SUCCESS

    def CloseFile_handle(self, *argus):
        # print("CloseFile_handle")
        return ntstatus.STATUS_SUCCESS

    def GetDiskFreeSpace_handle(self, *argus):
        # print("GetDiskFreeSpace_handle")
        free = 20 * 1024 * 1024 * 1024
        total = 20 * 1024 * 1024 * 1024
        argus[0][0] = c_ulonglong(free)
        argus[1][0] = c_ulonglong(total)
        argus[2][0] = c_ulonglong(free)
        return ntstatus.STATUS_SUCCESS

    def GetVolumeInformation_handle(self, *argus):
        # print("GetVolumeInformation_handle")
        sss = wintypes.LPWSTR(self.volume_name)
        memmove(argus[0], sss, len(sss.value) * 2)
        return ntstatus.STATUS_SUCCESS

    @operations_wrapper
    def ReadFile_handle(self, *argus):
        file_path = self.get_path_from_dokan_path(argus[0])
        buffer = argus[1].contents
        buffer_len = argus[2]
        read_len_buffer = argus[3]
        offset = argus[4]
        # print(F'file_path: {file_path}')
        # print(F'buffer_len: {buffer_len}')
        # print(F'offset: {offset}')
        if(self.path_is_exists(file_path)):
            filesize = None
            def callback(smb_fs: smbfs.SMBFS):
                nonlocal filesize
                smb_fs.getsize(file_path)
            self.get_fs(callback)
            # if(offset >= filesize):
            #     return ntstatus.STATUS_SUCCESS
            read_out = None
            def callback2(smb_fs: smbfs.SMBFS):
                nonlocal read_out
                f = smb_fs.open(file_path, "rb")
                f.seek(offset, 0)
                read_out = f.read(buffer_len)
                f.close()
            self.get_fs(callback2)
            
            read_out_len = len(read_out)
            # print(F"readout: {read_out}")
            # print(F"readoutlen: {read_out_len}")
            sss = create_string_buffer(read_out)
            # print(type(bytearray(read_out)))

            # sss = c_char * read_out_len
            # sss(b"222")
            memmove(buffer, pointer(sss), read_out_len)
            memmove(read_len_buffer, pointer(c_ulong(read_out_len)), sizeof(c_ulong))
        return ntstatus.STATUS_SUCCESS

    @operations_wrapper
    def WriteFile_handle(self, *argus):
        file_path = self.get_path_from_dokan_path(argus[0])
        buffer_len = argus[2]
        write_len_buffer = argus[3]
        offset = argus[4]
        DokanFileInfo = argus[5].contents
        # print((argus[1]))
        # print(type(argus[1]))
        # print(argus[1].contents)
        # print(id(argus[1].contents))
        # print(pointer(argus[1].contents))
        other_bytes = (c_char * buffer_len)()
        memmove(other_bytes, argus[1].contents, buffer_len)
        # print(other_bytes)
        byte_for_write = other_bytes
        WriteToEndOfFile = DokanFileInfo.WriteToEndOfFile
        
        write_len = None
        def callback(smb_fs: smbfs.SMBFS):
            nonlocal write_len
            f = smb_fs.open(file_path, "ab")
            f.seek(offset, 0)
            write_len = f.write(byte_for_write)
            f.close()
        self.get_fs(callback)
        
        memmove(write_len_buffer, pointer(c_ulong(write_len)), sizeof(c_ulong))
        # if(WriteToEndOfFile):
        #     print(f'file_path: {file_path}')
        #     print(f"NumberOfBytesToWrite: {buffer_len}")
        #     print(f"Offset: {offset}")
        #     print(f"WriteToEndOfFile: {WriteToEndOfFile}")
        #     print(f'数据大小: {len(byte_for_write)}')
        #     print(f'实际写入数量: {write_len}')
        return ntstatus.STATUS_SUCCESS

    def start(self):
        """启动dokan
        """
        _thread.start_new_thread(dokan_controller().dokan_start, ())
    
    def stop(self):
        """停止dokan
        """
        dokan_controller().dokan_stop()