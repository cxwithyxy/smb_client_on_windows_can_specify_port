import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from ctypes import *
import ctypes.wintypes as wintypes
import dokan.dokan_structure as dokan_structure

dokan = windll.LoadLibrary("C:\Windows\System32\dokan1.dll")
# print(a.DokanUnmount)
dokan_options = dokan_structure.builder().build_DOKAN_OPTIONS()
dokan_operations = dokan_structure.builder().build_DOKAN_OPERATIONS()


class sadasd():
    def ZwCreateFile_handle(self, b1,b2,b3,b4,b5,b6,b7,b8):
        print("ZwCreateFile")
        return 0

    def Cleanup_and_CloseFile(self, b1, b2):
        print("Cleanup_and_CloseFile")
        return 0

print(dokan_operations.class_dict)


# print("r u n")

# a = dokan.DokanMain(dokan_options, dokan_operations)

# # print(a)

# # dokan.DokanUnmount(c_wchar("K:/"))

# input("run finish waitting for ending")