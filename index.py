from file_io_emulation.Server import Server as FS_server

FS_server().start()
while(True):
    a = input("\n\nServer start ! enter q for exit \n======>\n")
    if(a == "stop"):
        FS_server().stop()
    if(a == "q"):
        break