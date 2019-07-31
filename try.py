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
        time.sleep(1)
        # lock.acquire()
        print(f"{threading.currentThread().ident}: {smbc.get_fs().getinfo('222.txt')}")
        # lock.release()
        # for walk_path in server_fs.walk.files("/", max_depth = 1):
        #     print(walk_path)

for i in range(0,4):
    threading.Thread(
        target = dododo,
        daemon = True
    ).start()
    print(f"#{i} thread start")
    # time.sleep(5)

while(True):
    a = input("\n\nServer start ! enter q for exit \n======>\n")
    if(a == "stop"):
        exit()
    if(a == "q"):
        break