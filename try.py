from fs.smbfs import smbfs
from my_lib.Config_controller.Config_controller import Config_controller as ConfC
import time
import threading
import random
from file_io_emulation.Smb_client import Smb_client

conf = ConfC('setting.ini')
conf.cd('smb')

smbc = Smb_client()


def dododo():
    
    while True:
        time.sleep(random.random())
        def mycallback(myfs: smbfs.SMBFS):
            print(myfs.getinfo("a.txt"))
        smbc.get_fs(mycallback)

for i in range(0,4):
    t = threading.Thread(
        target = dododo,
        daemon = True
    )
    t.start()
    print(f"#{t.ident} thread start")
    # time.sleep(5)

while(True):
    a = input("\n\nServer start ! enter q for exit \n======>\n")
    if(a == "stop"):
        exit()
    if(a == "q"):
        break