import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from ctypes import *
import ctypes.wintypes as wintypes
from dokan.Controller import Controller as dokan_controller

# print(a.DokanUnmount)
class sadasd():
    def ZwCreateFile_handle(self, b1,b2,b3,b4,b5,b6,b7,b8):
        print("ZwCreateFile")
        return 0

    def Cleanup_and_CloseFile(self, b1, b2):
        print("Cleanup_and_CloseFile")
        return 0

print("r u n")

dokan_controller().set_options("k")
dokan_controller().set_operations({
    "ZwCreateFile": sadasd().ZwCreateFile_handle,
    "Cleanup":sadasd().Cleanup_and_CloseFile,
    "CloseFile":sadasd().Cleanup_and_CloseFile,
})

dokan_controller().dokan_start()
# # print(a)

# # dokan.DokanUnmount(c_wchar("K:/"))

# input("run finish waitting for ending")