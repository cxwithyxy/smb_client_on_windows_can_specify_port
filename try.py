from fs.smbfs import smbfs
from my_lib.Config_controller.Config_controller import Config_controller as ConfC
import time
import threading
import random
from file_io_emulation.Smb_client import Smb_client

conf = ConfC('setting.ini')
conf.cd('smb')

smbc = Smb_client()


def dododo(aaa):
    
    while True:
        time.sleep(random.random())
        def mycallback(myfs: smbfs.SMBFS):
            print(myfs.getinfo("a.txt"))
        smbc.get_fs(mycallback)
        dddd=9
        twowowo = None
        def mycallback2(myfs: smbfs.SMBFS):
            nonlocal twowowo
            twowowo = (myfs.getinfo("222.txt"))
            print(dddd)
        smbc.get_fs(mycallback2)
        print(twowowo)

def sub_do():
    for i in range(0, 2):
        t = threading.Thread(
            target = dododo,
            args = (3,),
            daemon = True
        )
        t.start()
        print(f"#{t.ident} subthread start from{threading.currentThread().ident}")

for i in range(0, 4):
    t = threading.Thread(
        target = sub_do,
        daemon = True
    )
    t.start()
    print(f"#{t.ident} thread start")

while(True):
    a = input("\n\nServer start ! enter q for exit \n======>\n")
    if(a == "stop"):
        exit()
    if(a == "q"):
        break