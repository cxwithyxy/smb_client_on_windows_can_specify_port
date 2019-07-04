from ctypes import *
from PythonSingleton.Singleton import Singleton as SLT
import ctypes.wintypes as wintypes
import dokan.dokan_structure as dokan_structure

class Controller(SLT):
    
    dokan_dll = None
    dokan_options = None
    dokan_operations = None

    
    def __Singleton_Init__(self):
        self.dokan_dll = windll.LoadLibrary("C:\Windows\System32\dokan1.dll")
        print("load dll end")

    def set_operations(self, callback_dict = {}):
        """设置dokan回调操作

        Args: 
            
            callback_dict: 回调函数字典，对应在dokan.h中DOKAN_OPERATIONS结构体的函数及其名称
        """
        self.dokan_operations = dokan_structure.Builder().build_DOKAN_OPERATIONS(callback_dict)

    def set_options(self, mount_point):
        """设置dokan配置

        Args:
            
            mount_point: 挂载点, 如k, 代表挂载成k盘
        """
        self.dokan_options = dokan_structure.Builder().build_DOKAN_OPTIONS(mount_point)

    def dokan_start(self):
        """启动dokan
        """
        if not self.dokan_options:
            raise BaseException("dokan_options have not set, pls call set_options")
        if not self.dokan_operations:
            raise BaseException("dokan_operations have not set , pls call set_operations")
        self.dokan_dll.DokanMain(self.dokan_options, self.dokan_operations)

    def dokan_stop(self):
        """停止dokan
        """
        self.dokan_dll.DokanRemoveMountPoint(self.dokan_options.MountPoint, wintypes.BOOL(True))