from fs.smbfs import smbfs
from my_lib.Config_controller.Config_controller import Config_controller as ConfC
import time
import threading
import random

conf = ConfC('setting.ini')
conf.cd('smb')


lock = threading.Lock()

def dododo():
    smb_fs = smbfs.SMBFS(
        conf.get('ip'),
        username = conf.get('username'),
        passwd = conf.get('passwd'),
        timeout = 5,
        port = int(conf.get('port')),
        direct_tcp = int(conf.get('direct_tcp'))
    )
    server_fs = smb_fs.opendir(conf.get('enter_path'))
    while True:
        time.sleep(1)
        # lock.acquire()
        print(f"{threading.currentThread().ident}: {server_fs.getinfo('222.txt')}")
        # lock.release()
        # for walk_path in server_fs.walk.files("/", max_depth = 1):
        #     print(walk_path)

for i in range(0,5):
    threading.Thread(
        target = dododo,
        daemon = True
    ).start()
    print(f"#{i} thread start")
    time.sleep(5)

while(True):
    a = input("\n\nServer start ! enter q for exit \n======>\n")
    if(a == "stop"):
        exit()
    if(a == "q"):
        break