import threading
from my_lib.Config_controller.Config_controller import Config_controller as ConfC
from fs.smbfs import smbfs

class Smbfs_controller:
    
    is_using: bool = False
    smb_fs: smbfs.SMBFS

    def __init__(self, smb_fs: smbfs.SMBFS):
        self.smb_fs = smb_fs

    def get_smb_fs(self):
        return self.smb_fs

    def using(self):
        self.is_using = True

    def un_using(self):
        self.is_using = False

class Smb_client:

    smb_fs_count = 1
    smb_fss = []
    conf: ConfC
    thread_lock: threading.RLock
    
    def __init__(self):
        self.thread_lock = threading.RLock()
        self.conf = ConfC('setting.ini')
        self.conf.cd('smb')
        self.smb_fs_count = int(self.conf.get("connection_count"))
        for i in range(0, self.smb_fs_count):
            self.create_smb_fs()

    def create_smb_fs(self):
        smb_fs = smbfs.SMBFS(
            self.conf.get('ip'),
            username = self.conf.get('username'),
            passwd = self.conf.get('passwd'),
            timeout = 5,
            port = int(self.conf.get('port')),
            direct_tcp = int(self.conf.get('direct_tcp'))
        )
        smb_fs = smb_fs.opendir(self.conf.get('enter_path'))
        self.smb_fss.append(Smbfs_controller(smb_fs))
    
    def get_free_fs(self) -> Smbfs_controller:
        re_val = False
        for i in self.smb_fss:
            if not i.is_using:
                re_val = i
                break
        return re_val
    
    def wait_until_free_fs(self) -> Smbfs_controller:
        free_fs = [None]
        while True:
            free_fs[0] = self.get_free_fs()
            if free_fs[0]:
                break
        return free_fs[0]

    def get_fs(self, callback):
        self.thread_lock.acquire()
        free_fs = self.wait_until_free_fs()
        free_fs.using()
        # print(f"{threading.currentThread().ident}: get {id(free_fs)}")
        self.thread_lock.release()
        callback(free_fs.get_smb_fs())
        free_fs.un_using()
