import time
import fs.zipfs as zipfs
import fs.mountfs as mountfs
from ctypes import *
import dokan.dokan_structure as dokan_structure

dokan = windll.LoadLibrary("C:\Windows\System32\dokan1.dll")
# print(a.DokanUnmount)

dokan_options = dokan_structure.DOKAN_OPTIONS()

dokan_options.Version = 122
# dokan_options.ThreadCount = 1
# dokan_options.Options = 1
dokan_options.MountPoint = c_wchar_p("K:\\")
# dokan_options.UNCName = c_wchar_p("")
# dokan_options.Timeout = 5 * 1000
# dokan_options.AllocationUnitSize = 10 * 1024 * 1024
# dokan_options.SectorSize = 10 * 1024 * 1024

dokan_operations = dokan_structure.DOKAN_OPERATIONS()

print("r u n")

a = dokan.DokanMain(dokan_options, dokan_operations)

print(a)

# dokan.DokanUnmount(c_wchar("K:/"))