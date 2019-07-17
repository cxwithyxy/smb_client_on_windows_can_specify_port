from file_io_emulation.Server import Server as FS_server

FS_server().start()
while(True):
    a = input("==>\n")
    if(a == "stop"):
        FS_server().stop()
    if(a == "q"):
        break


# from ctypes import *
# import ctypes.wintypes as wintypes

# a = windll.LoadLibrary("kernel32.dll")
# GetShortPathName = a.GetShortPathNameW
# print(a)
# the_input = create_string_buffer(b"cxcxcxcxcxcxc.txt")
# the_output = create_string_buffer(200)
# print(the_output.value)
# a.GetShortPathNameW(the_input, the_output, wintypes.DWORD(14))
# print(the_output.value)

# import win32.win32api as win32api
# a = win32api.GetShortPathName("M:\\kaikengqi.docx")
# print(a)