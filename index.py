from file_io_emulation.Server import Server as FS_server

# FS_server()
FS_server().start()
while(True):
    a = input("==>\n")
    if(a == "stop"):
        FS_server().stop()
    if(a == "q"):
        break


# from ctypes import *
# import ctypes.wintypes as wintypes

# sssa = create_string_buffer(b"12345679")
# sss = cast(sssa, c_void_p)
# print(type(sss.value))

# sss = pointer(sss)
# print(type(sss.contents))

# memmove(sss.contents, create_string_buffer(b"1111111"), 10)
# sss = cast(sss.contents, c_char_p)
# print(sss.value)