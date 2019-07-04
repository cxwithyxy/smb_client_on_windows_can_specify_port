from dokan.Controller import Controller as dokan_controller
from PythonSingleton.Singleton import Singleton as SLT

class Server(SLT):

    def __init__(self):
        dokan_controller().set_options("k")
        dokan_controller().set_operations({
            "ZwCreateFile": self.ZwCreateFile_handle,
            "Cleanup":self.Cleanup_and_CloseFile,
            "CloseFile":self.Cleanup_and_CloseFile,
        })

    def start(self):
        print("sssstart")
        dokan_controller().dokan_start()

    def ZwCreateFile_handle(self, b1,b2,b3,b4,b5,b6,b7,b8):
        print("ZwCreateFile")
        return 0
    
    def Cleanup_and_CloseFile(self, b1, b2):
        print("Cleanup_and_CloseFile")
        return 0