import threading
from my_lib.Config_controller.Config_controller import Config_controller as ConfC
from fs.smbfs import smbfs

class Smb_client:

    smb_fss = {}
    conf: ConfC
    
    def __init__(self):
        self.conf = ConfC('setting.ini')
        self.conf.cd('smb')

    def get_thread_id(self):
        return threading.currentThread().ident

    def create_smb_fs(self, thread_id: int):
        smb_fs = smbfs.SMBFS(
            self.conf.get('ip'),
            username = self.conf.get('username'),
            passwd = self.conf.get('passwd'),
            timeout = 5,
            port = int(self.conf.get('port')),
            direct_tcp = int(self.conf.get('direct_tcp'))
        )
        smb_fs = smb_fs.opendir(self.conf.get('enter_path'))
        self.smb_fss[str(thread_id)] = smb_fs
        print(f"T#{thread_id}")
        return smb_fs
        
    def get_fs(self):
        try:
            return self.smb_fss[str(self.get_thread_id())]
        except KeyError as e:
            return self.create_smb_fs(self.get_thread_id())
