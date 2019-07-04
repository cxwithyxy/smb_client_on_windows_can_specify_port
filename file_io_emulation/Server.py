from dokan.Controller import Controller as dokan_controller
from PythonSingleton.Singleton import Singleton as SLT
import _thread

class Server(SLT):

    def __Singleton_Init__(self):
        dokan_controller().set_options("k")
        dokan_controller().set_operations({
            "ZwCreateFile": self.ZwCreateFile_handle,
            "Cleanup":self.Cleanup_and_CloseFile,
            "CloseFile":self.Cleanup_and_CloseFile,
        })

    def start(self):
        """启动dokan
        """
        _thread.start_new_thread(dokan_controller().dokan_start, ())

    def stop(self):
        """停止dokan
        """
        dokan_controller().dokan_stop()

    def ZwCreateFile_handle(self, b1,b2,b3,b4,b5,b6,b7,b8):
        print("ZwCreateFile")
        return 0
    
    def Cleanup_and_CloseFile(self, b1, b2):
        print("Cleanup_and_CloseFile")
        return 0